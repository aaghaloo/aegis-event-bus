#!/usr/bin/env python3
"""
Monitoring alerts configuration for Aegis Event Bus.
Sets up alerts for critical system events.
"""

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List

import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MonitoringAlerts:
    """Configure and manage monitoring alerts."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.alert_config = self._load_alert_config()

    def _load_alert_config(self) -> Dict[str, Any]:
        """Load alert configuration."""
        config_file = Path("config/alerts.json")
        if config_file.exists():
            with open(config_file, "r") as f:
                return json.load(f)
        else:
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default alert configuration."""
        return {
            "health_checks": {
                "api_timeout": 5,
                "database_timeout": 10,
                "mqtt_timeout": 15,
            },
            "performance_thresholds": {
                "response_time_ms": 2000,
                "error_rate_percent": 5,
                "cpu_percent": 80,
                "memory_percent": 85,
                "disk_percent": 90,
            },
            "security_alerts": {
                "auth_failures_per_hour": 10,
                "rate_limit_violations_per_hour": 50,
                "suspicious_ips": [],
            },
            "notifications": {"email": [], "slack": "", "webhook": ""},
        }

    def check_health_alerts(self) -> List[Dict[str, Any]]:
        """Check for health-related alerts."""
        alerts = []

        try:
            # Check API health
            start_time = time.time()
            response = requests.get(f"{self.base_url}/healthz", timeout=5)
            api_time = (time.time() - start_time) * 1000

            if response.status_code != 200:
                alerts.append(
                    {
                        "level": "CRITICAL",
                        "type": "health",
                        "message": f"API health check failed: {response.status_code}",
                        "timestamp": time.time(),
                    }
                )
            elif api_time > self.alert_config["health_checks"]["api_timeout"] * 1000:
                alerts.append(
                    {
                        "level": "WARNING",
                        "type": "performance",
                        "message": f"API response time slow: {api_time:.0f}ms",
                        "timestamp": time.time(),
                    }
                )

            # Check comprehensive health
            response = requests.get(
                f"{self.base_url}/healthz/comprehensive", timeout=10
            )
            if response.status_code == 200:
                health_data = response.json()

                if health_data.get("overall_status") != "healthy":
                    alerts.append(
                        {
                            "level": "CRITICAL",
                            "type": "health",
                            "message": f"System health degraded: {health_data.get('overall_status')}",
                            "timestamp": time.time(),
                        }
                    )

                # Check individual components
                checks = health_data.get("checks", {})
                for component, status in checks.items():
                    if status.get("status") != "healthy":
                        component_status = status.get("status")
                        alerts.append(
                            {
                                "level": "WARNING",
                                "type": "health",
                                "message": f"{component} component unhealthy: {component_status}",
                                "timestamp": time.time(),
                            }
                        )

        except requests.exceptions.RequestException as e:
            alerts.append(
                {
                    "level": "CRITICAL",
                    "type": "connectivity",
                    "message": f"Unable to reach API: {str(e)}",
                    "timestamp": time.time(),
                }
            )

        return alerts

    def check_performance_alerts(self) -> List[Dict[str, Any]]:
        """Check for performance-related alerts."""
        alerts = []

        try:
            # Get performance metrics
            response = requests.get(f"{self.base_url}/metrics/performance", timeout=5)
            if response.status_code == 200:
                metrics = response.json()

                # Check response time
                avg_response_time = metrics.get("avg_response_time", 0)
                threshold = self.alert_config["performance_thresholds"]["response_time_ms"]
                if avg_response_time > threshold:
                    alerts.append(
                        {
                            "level": "WARNING",
                            "type": "performance",
                            "message": f"High average response time: {avg_response_time:.0f}ms",
                            "timestamp": time.time(),
                        }
                    )

                # Check error rate
                error_rate = metrics.get("error_rate", 0) * 100
                error_threshold = self.alert_config["performance_thresholds"]["error_rate_percent"]
                if error_rate > error_threshold:
                    alerts.append(
                        {
                            "level": "WARNING",
                            "type": "performance",
                            "message": f"High error rate: {error_rate:.1f}%",
                            "timestamp": time.time(),
                        }
                    )

            # Get system metrics
            response = requests.get(f"{self.base_url}/metrics/system", timeout=5)
            if response.status_code == 200:
                system_metrics = response.json()

                # Check CPU usage
                cpu_percent = system_metrics.get("cpu_percent", 0)
                cpu_threshold = self.alert_config["performance_thresholds"]["cpu_percent"]
                if cpu_percent > cpu_threshold:
                    alerts.append(
                        {
                            "level": "WARNING",
                            "type": "resource",
                            "message": f"High CPU usage: {cpu_percent:.1f}%",
                            "timestamp": time.time(),
                        }
                    )

                # Check memory usage
                memory_percent = system_metrics.get("memory_percent", 0)
                memory_threshold = self.alert_config["performance_thresholds"]["memory_percent"]
                if memory_percent > memory_threshold:
                    alerts.append(
                        {
                            "level": "WARNING",
                            "type": "resource",
                            "message": f"High memory usage: {memory_percent:.1f}%",
                            "timestamp": time.time(),
                        }
                    )

                # Check disk usage
                disk_percent = system_metrics.get("disk_percent", 0)
                if (
                    disk_percent
                    > self.alert_config["performance_thresholds"]["disk_percent"]
                ):
                    alerts.append(
                        {
                            "level": "WARNING",
                            "type": "resource",
                            "message": f"High disk usage: {disk_percent:.1f}%",
                            "timestamp": time.time(),
                        }
                    )

        except requests.exceptions.RequestException as e:
            alerts.append(
                {
                    "level": "WARNING",
                    "type": "monitoring",
                    "message": f"Unable to fetch metrics: {str(e)}",
                    "timestamp": time.time(),
                }
            )

        return alerts

    def check_security_alerts(self) -> List[Dict[str, Any]]:
        """Check for security-related alerts."""
        alerts = []

        try:
            # Check certificate health
            response = requests.get(
                f"{self.base_url}/healthz/comprehensive", timeout=10
            )
            if response.status_code == 200:
                health_data = response.json()
                cert_status = health_data.get("checks", {}).get("certificates", {})

                if cert_status.get("status") == "critical":
                    alerts.append(
                        {
                            "level": "CRITICAL",
                            "type": "security",
                            "message": "SSL certificates expired or invalid",
                            "timestamp": time.time(),
                        }
                    )
                elif cert_status.get("status") == "warning":
                    alerts.append(
                        {
                            "level": "WARNING",
                            "type": "security",
                            "message": "SSL certificates expiring soon",
                            "timestamp": time.time(),
                        }
                    )

        except requests.exceptions.RequestException as e:
            alerts.append(
                {
                    "level": "WARNING",
                    "type": "monitoring",
                    "message": f"Unable to check security status: {str(e)}",
                    "timestamp": time.time(),
                }
            )

        return alerts

    def send_notification(self, alert: Dict[str, Any]):
        """Send alert notification."""
        try:
            # Log alert
            logger.warning(f"Alert: {alert['level']} - {alert['message']}")

            # Send to webhook if configured
            webhook_url = self.alert_config["notifications"].get("webhook")
            if webhook_url:
                payload = {
                    "text": f"[{alert['level']}] {alert['message']}",
                    "timestamp": alert["timestamp"],
                    "type": alert["type"],
                }
                requests.post(webhook_url, json=payload, timeout=5)

            # Send to Slack if configured
            slack_webhook = self.alert_config["notifications"].get("slack")
            if slack_webhook:
                payload = {
                    "text": f"🚨 [{alert['level']}] {alert['message']}",
                    "channel": "#alerts",
                }
                requests.post(slack_webhook, json=payload, timeout=5)

            # Send email if configured
            email_list = self.alert_config["notifications"].get("email", [])
            if email_list and alert["level"] in ["CRITICAL", "WARNING"]:
                # Implement email sending logic here
                pass

        except Exception as e:
            logger.error(f"Failed to send notification: {str(e)}")

    def run_alert_check(self):
        """Run complete alert check."""
        all_alerts = []

        # Check health alerts
        all_alerts.extend(self.check_health_alerts())

        # Check performance alerts
        all_alerts.extend(self.check_performance_alerts())

        # Check security alerts
        all_alerts.extend(self.check_security_alerts())

        # Send notifications for critical alerts
        for alert in all_alerts:
            if alert["level"] in ["CRITICAL", "WARNING"]:
                self.send_notification(alert)

        return all_alerts


def main():
    """Main function for alert monitoring."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Monitoring alerts for Aegis Event Bus"
    )
    parser.add_argument("--url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--config", help="Alert configuration file")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    parser.add_argument(
        "--interval", type=int, default=60, help="Check interval in seconds"
    )

    args = parser.parse_args()

    # Initialize monitoring
    monitor = MonitoringAlerts(args.url)

    if args.daemon:
        logger.info("Starting monitoring daemon...")
        while True:
            try:
                alerts = monitor.run_alert_check()
                if alerts:
                    logger.info(f"Found {len(alerts)} alerts")
                time.sleep(args.interval)
            except KeyboardInterrupt:
                logger.info("Monitoring daemon stopped")
                break
            except Exception as e:
                logger.error(f"Monitoring error: {str(e)}")
                time.sleep(args.interval)
    else:
        # Single check
        alerts = monitor.run_alert_check()
        if alerts:
            logger.info(f"Found {len(alerts)} alerts:")
            for alert in alerts:
                logger.info(f"  [{alert['level']}] {alert['message']}")
        else:
            logger.info("No alerts found")


if __name__ == "__main__":
    main()
