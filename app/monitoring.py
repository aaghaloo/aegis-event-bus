# app/monitoring.py
"""
Monitoring and observability module.
Provides performance metrics, health checks, and system monitoring.
"""

import time
from collections import defaultdict, deque
from datetime import datetime
from typing import Any, Dict

import psutil
import structlog

from .config import settings

log = structlog.get_logger(__name__)


class PrometheusMetrics:
    """Prometheus-style metrics collection."""

    def __init__(self):
        self.metrics = {
            "http_requests_total": defaultdict(int),
            "http_request_duration_seconds": deque(maxlen=1000),
            "http_requests_in_progress": 0,
            "database_connections_active": 0,
            "database_connections_idle": 0,
            "task_creation_total": defaultdict(int),
            "task_completion_total": defaultdict(int),
            "agent_heartbeats_total": defaultdict(int),
            "agent_registrations_total": defaultdict(int),
        }

    def record_http_request(
        self, method: str, path: str, status_code: int, duration: float
    ):
        """Record HTTP request metrics."""
        self.metrics["http_requests_total"][f"{method}_{path}_{status_code}"] += 1
        self.metrics["http_request_duration_seconds"].append(duration)

    def record_task_creation(self, agent_id: str, status: str):
        """Record task creation metrics."""
        self.metrics["task_creation_total"][f"{agent_id}_{status}"] += 1

    def record_task_completion(self, agent_id: str, status: str):
        """Record task completion metrics."""
        self.metrics["task_completion_total"][f"{agent_id}_{status}"] += 1

    def record_agent_heartbeat(self, agent_id: str):
        """Record agent heartbeat metrics."""
        self.metrics["agent_heartbeats_total"][agent_id] += 1

    def record_agent_registration(self, agent_id: str):
        """Record agent registration metrics."""
        self.metrics["agent_registrations_total"][agent_id] += 1

    def update_database_metrics(self, active: int, idle: int):
        """Update database connection metrics."""
        self.metrics["database_connections_active"] = active
        self.metrics["database_connections_idle"] = idle

    def get_prometheus_format(self) -> str:
        """Export metrics in Prometheus format."""
        lines = []

        # HTTP request metrics
        for key, count in self.metrics["http_requests_total"].items():
            lines.append(f'http_requests_total{{method="{key}"}} {count}')

        # HTTP duration metrics
        if self.metrics["http_request_duration_seconds"]:
            durations = list(self.metrics["http_request_duration_seconds"])
            avg_duration = sum(durations) / len(durations)
            lines.append(f"http_request_duration_seconds_avg {avg_duration}")
            lines.append(f"http_request_duration_seconds_max {max(durations)}")

        # Database metrics
        lines.append(
            f'database_connections_active {self.metrics["database_connections_active"]}'
        )
        lines.append(
            f'database_connections_idle {self.metrics["database_connections_idle"]}'
        )

        # Task metrics
        for key, count in self.metrics["task_creation_total"].items():
            lines.append(f'task_creation_total{{agent_status="{key}"}} {count}')

        for key, count in self.metrics["task_completion_total"].items():
            lines.append(f'task_completion_total{{agent_status="{key}"}} {count}')

        # Agent metrics
        for agent_id, count in self.metrics["agent_heartbeats_total"].items():
            lines.append(f'agent_heartbeats_total{{agent_id="{agent_id}"}} {count}')

        for agent_id, count in self.metrics["agent_registrations_total"].items():
            lines.append(f'agent_registrations_total{{agent_id="{agent_id}"}} {count}')

        return "\n".join(lines)


class PerformanceMonitor:
    """Monitor application performance and resource usage."""

    def __init__(self):
        self.request_times = deque(maxlen=1000)
        self.error_counts = defaultdict(int)
        self.start_time = datetime.now()
        self._last_gc_stats = None
        self.prometheus_metrics = PrometheusMetrics()

    def record_request(self, method: str, path: str, status_code: int, duration: float):
        """Record a request for performance monitoring."""
        self.request_times.append(
            {
                "method": method,
                "path": path,
                "status_code": status_code,
                "duration": duration,
                "timestamp": datetime.now(),
            }
        )

        # Record Prometheus metrics
        self.prometheus_metrics.record_http_request(method, path, status_code, duration)

        # Log slow requests
        if duration > 1.0:  # More than 1 second
            log.warning(
                "slow_request",
                method=method,
                path=path,
                duration=duration,
                status_code=status_code,
            )

        # Log errors
        if status_code >= 400:
            self.error_counts[f"{status_code}"] += 1
            log.error(
                "request_error",
                method=method,
                path=path,
                status_code=status_code,
                duration=duration,
            )

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics."""
        if not self.request_times:
            return {"message": "No requests recorded yet"}

        durations = [req["duration"] for req in self.request_times]
        status_codes = [req["status_code"] for req in self.request_times]

        return {
            "total_requests": len(self.request_times),
            "avg_response_time": sum(durations) / len(durations),
            "min_response_time": min(durations),
            "max_response_time": max(durations),
            "error_rate": len([s for s in status_codes if s >= 400])
            / len(status_codes),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "error_counts": dict(self.error_counts),
        }

    def get_system_stats(self) -> Dict[str, Any]:
        """Get system resource usage statistics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": memory.available / (1024**3),
                "disk_percent": disk.percent,
                "disk_free_gb": disk.free / (1024**3),
            }
        except Exception as e:
            log.error("system_stats_error", error=str(e))
            return {"error": "Could not retrieve system stats"}


class HealthChecker:
    """Comprehensive health checking for all system components."""

    def __init__(self):
        self.performance_monitor = PerformanceMonitor()

    def check_database_health(self) -> Dict[str, Any]:
        """Check database connectivity and performance."""
        try:
            from .db import engine_rw

            start_time = time.time()

            # Simple connection test
            with engine_rw.connect() as conn:
                result = conn.execute("SELECT 1")
                result.fetchone()

            duration = time.time() - start_time

            # Update Prometheus metrics
            pool = engine_rw.pool
            self.performance_monitor.prometheus_metrics.update_database_metrics(
                active=pool.checkedout(), idle=pool.checkedin()
            )

            return {
                "status": "healthy",
                "response_time": duration,
                "connection_pool_size": pool.size(),
                "connection_pool_checked_in": pool.checkedin(),
                "connection_pool_checked_out": pool.checkedout(),
                "connection_pool_overflow": pool.overflow(),
            }
        except Exception as e:
            log.error("database_health_check_failed", error=str(e))
            return {"status": "unhealthy", "error": str(e)}

    def check_mqtt_health(self) -> Dict[str, Any]:
        """Check MQTT connectivity."""
        try:
            import paho.mqtt.publish as mqtt_publish

            from .cert_manager import cert_manager

            start_time = time.time()

            # Test MQTT connection
            tls_config = cert_manager.get_mqtt_tls_config()
            mqtt_publish.single(
                topic="health/test",
                payload="test",
                hostname=settings.MQTT_HOST,
                port=settings.MQTT_PORT,
                tls=tls_config,
                keepalive=5,
            )

            duration = time.time() - start_time

            return {
                "status": "healthy",
                "response_time": duration,
                "host": settings.MQTT_HOST,
                "port": settings.MQTT_PORT,
            }
        except Exception as e:
            log.error("mqtt_health_check_failed", error=str(e))
            return {"status": "unhealthy", "error": str(e)}

    def check_certificate_health(self) -> Dict[str, Any]:
        """Check certificate validity and expiry."""
        try:
            from .cert_manager import cert_manager

            cert_status = cert_manager.validate_certificate_expiry()

            # Check if any certificates are expired or expiring soon
            expired_certs = []
            expiring_certs = []

            for cert_name, info in cert_status.items():
                if info and info.get("is_expired", False):
                    expired_certs.append(cert_name)
                elif info and info.get("is_expiring_soon", False):
                    expiring_certs.append(cert_name)

            status = "healthy"
            if expired_certs:
                status = "critical"
            elif expiring_certs:
                status = "warning"

            return {
                "status": status,
                "certificates": cert_status,
                "expired_certificates": expired_certs,
                "expiring_certificates": expiring_certs,
            }
        except Exception as e:
            log.error("certificate_health_check_failed", error=str(e))
            return {"status": "unhealthy", "error": str(e)}

    def comprehensive_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check of all components."""
        start_time = time.time()

        health_results = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "checks": {
                "database": self.check_database_health(),
                "mqtt": self.check_mqtt_health(),
                "certificates": self.check_certificate_health(),
                "system": self.performance_monitor.get_system_stats(),
            },
        }

        # Determine overall status
        unhealthy_checks = [
            name
            for name, result in health_results["checks"].items()
            if result.get("status") in ["unhealthy", "critical"]
        ]

        if unhealthy_checks:
            health_results["overall_status"] = "unhealthy"
            health_results["unhealthy_components"] = unhealthy_checks

        health_results["check_duration"] = time.time() - start_time

        return health_results


# Global instances
performance_monitor = PerformanceMonitor()
health_checker = HealthChecker()
