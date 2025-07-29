# app/cert_manager.py
"""
Certificate management and rotation system.
Handles MQTT certificates and other TLS certificates.
"""

import ssl
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import structlog
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

log = structlog.get_logger(__name__)


class CertificateManager:
    """Manages certificates for the application."""

    def __init__(self):
        self.cert_dir = Path("./mosquitto/certs")
        self.ca_cert_path = self.cert_dir / "ca.crt"
        self.client_cert_path = self.cert_dir / "client.crt"
        self.client_key_path = self.cert_dir / "client.key"

    def get_ssl_context(self) -> Optional[ssl.SSLContext]:
        """Get SSL context for MQTT connections."""
        if not self.ca_cert_path.exists():
            log.warning("ca_cert_not_found", path=str(self.ca_cert_path))
            return None

        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_verify_locations(str(self.ca_cert_path))

            if self.client_cert_path.exists() and self.client_key_path.exists():
                context.load_cert_chain(
                    str(self.client_cert_path), str(self.client_key_path)
                )

            return context
        except Exception as e:
            log.error("ssl_context_creation_failed", error=str(e))
            return None

    def validate_certificate_expiry(self) -> Dict[str, Any]:
        """Check if certificates are expiring soon."""
        results = {
            "ca_cert": self._check_cert_expiry(self.ca_cert_path),
            "client_cert": self._check_cert_expiry(self.client_cert_path),
        }

        # Log warnings for expiring certificates
        for cert_name, info in results.items():
            if info and info.get("days_until_expiry", 0) < 30:
                log.warning(
                    "certificate_expiring_soon",
                    cert_name=cert_name,
                    days_until_expiry=info.get("days_until_expiry"),
                    expiry_date=info.get("expiry_date"),
                )

        return results

    def _check_cert_expiry(self, cert_path: Path) -> Optional[Dict[str, Any]]:
        """Check expiry for a specific certificate."""
        if not cert_path.exists():
            return None

        try:
            with open(cert_path, "rb") as f:
                cert_data = f.read()

            cert = x509.load_pem_x509_certificate(cert_data)
            expiry_date = cert.not_valid_after
            days_until_expiry = (expiry_date - datetime.now()).days

            return {
                "expiry_date": expiry_date.isoformat(),
                "days_until_expiry": days_until_expiry,
                "is_expired": days_until_expiry < 0,
                "is_expiring_soon": days_until_expiry < 30,
            }
        except Exception as e:
            log.error(
                "cert_expiry_check_failed", cert_path=str(cert_path), error=str(e)
            )
            return None

    def generate_self_signed_cert(self, common_name: str, days: int = 365) -> bool:
        """Generate a self-signed certificate for development."""
        try:
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )

            # Create certificate
            subject = issuer = x509.Name(
                [
                    x509.NameAttribute(NameOID.COMMON_NAME, common_name),
                    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Aegis Event Bus"),
                    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                ]
            )

            cert = (
                x509.CertificateBuilder()
                .subject_name(subject)
                .issuer_name(issuer)
                .public_key(private_key.public_key())
                .serial_number(x509.random_serial_number())
                .not_valid_before(datetime.utcnow())
                .not_valid_after(datetime.utcnow() + timedelta(days=days))
                .add_extension(
                    x509.SubjectAlternativeName(
                        [
                            x509.DNSName(common_name),
                            x509.IPAddress("127.0.0.1"),
                        ]
                    ),
                    critical=False,
                )
                .sign(private_key, hashes.SHA256())
            )

            # Ensure cert directory exists
            self.cert_dir.mkdir(parents=True, exist_ok=True)

            # Write certificate
            with open(self.ca_cert_path, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))

            # Write private key
            with open(self.client_key_path, "wb") as f:
                f.write(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption(),
                    )
                )

            log.info("self_signed_cert_generated", common_name=common_name, days=days)
            return True

        except Exception as e:
            log.error("cert_generation_failed", error=str(e))
            return False

    def get_mqtt_tls_config(self) -> Optional[Dict[str, Any]]:
        """Get TLS configuration for MQTT."""
        if not self.ca_cert_path.exists():
            return None

        return {
            "ca_certs": str(self.ca_cert_path),
            "certfile": (
                str(self.client_cert_path) if self.client_cert_path.exists() else None
            ),
            "keyfile": (
                str(self.client_key_path) if self.client_key_path.exists() else None
            ),
        }


# Global certificate manager instance
cert_manager = CertificateManager()
