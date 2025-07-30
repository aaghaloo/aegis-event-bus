# app/security_config.py
"""
Security configuration for the application.
Defines security headers, CSP policies, and security middleware.
"""

from typing import Dict

# Security headers configuration
SECURITY_HEADERS: Dict[str, str] = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
}

# Content Security Policy
CSP_POLICY = {
    "default-src": ["'self'"],
    "script-src": ["'self'", "'unsafe-inline'"],
    "style-src": ["'self'", "'unsafe-inline'"],
    "img-src": ["'self'", "data:", "https:"],
    "font-src": ["'self'"],
    "connect-src": ["'self'"],
    "frame-src": ["'none'"],
    "object-src": ["'none'"],
    "base-uri": ["'self'"],
    "form-action": ["'self'"],
}

# Rate limiting configuration
RATE_LIMIT_CONFIG = {
    "default": "100/minute",
    "auth": "5/minute",
    "api": "1000/minute",
    "health": "60/minute",
}

# Input validation patterns
SECURITY_PATTERNS = {
    "sql_injection": [
        r"(\b(union|select|insert|update|delete|drop|create|alter)\b)",
        r"(\b(exec|execute|sp_|xp_)\b)",
        r"(--|#|/\*|\*/)",
        r"(\b(and|or)\b\s+\d+\s*[=<>])",
    ],
    "path_traversal": [
        r"(\.\./|\.\.\\)",
        r"(/%2e%2e/|%2e%2e/)",
        r"(\\x2e\\x2e|\\x2e\\x2e)",
    ],
    "script_injection": [
        r"(<script[^>]*>.*?</script>)",
        r"(javascript:)",
        r"(on\w+\s*=)",
        r"(vbscript:)",
        r"(<iframe[^>]*>)",
    ],
}

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {
    "text": [".txt", ".md", ".json", ".xml", ".csv"],
    "image": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "document": [".pdf", ".doc", ".docx"],
    "archive": [".zip", ".tar", ".gz"],
}

# Maximum file sizes (in bytes)
MAX_FILE_SIZES = {
    "text": 1024 * 1024,  # 1MB
    "image": 5 * 1024 * 1024,  # 5MB
    "document": 10 * 1024 * 1024,  # 10MB
    "archive": 50 * 1024 * 1024,  # 50MB
}

# Session security configuration
SESSION_CONFIG = {
    "max_age": 3600,  # 1 hour
    "secure": True,
    "httponly": True,
    "samesite": "strict",
}

# Password policy
PASSWORD_POLICY = {
    "min_length": 8,
    "require_uppercase": True,
    "require_lowercase": True,
    "require_digits": True,
    "require_special": True,
    "max_age_days": 90,
    "history_count": 5,
}

# Account lockout policy
LOCKOUT_POLICY = {
    "max_attempts": 5,
    "lockout_duration_minutes": 30,
    "reset_after_hours": 24,
}

# API security
API_SECURITY = {
    "max_payload_size": 10 * 1024 * 1024,  # 10MB
    "max_depth": 10,
    "max_items": 1000,
    "timeout_seconds": 30,
}

# CORS configuration
CORS_CONFIG = {
    "allow_origins": ["http://localhost:3000", "https://yourdomain.com"],
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["*"],
    "max_age": 3600,
}
