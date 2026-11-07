"""Deterministic toy detections for synthetic lab events."""

import re


PATTERNS = {
    "vpn_anomalous_login": lambda event: event.get("type") == "vpn_login" and (
        event.get("hour", 12) < 6 or event.get("source_zone") == "external_untrusted"
    ),
    "sql_injection_pattern": lambda event: event.get("type") == "http_request" and bool(
        re.search(r"(union\s+select|or\s+['\"]?1['\"]?\s*=\s*['\"]?1|--|/\*)", event.get("query", ""), re.I)
    ),
    "invalid_device_certificate": lambda event: event.get("type") == "mqtt_connect" and not event.get("certificate_valid", False),
    "actuator_out_of_profile": lambda event: event.get("type") == "actuator_command" and (
        event.get("hour", 12) not in range(6, 22) or event.get("profile") != "approved"
    ),
}


def detect(event):
    return [name for name, rule in PATTERNS.items() if rule(event)]
