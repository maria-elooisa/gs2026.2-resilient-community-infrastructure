import os
import tempfile
import unittest

from app.database import fixed_search, initialize, vulnerable_search
from detection.rules import detect
from edge.store_forward import CloudSink, EdgeBuffer, reconcile


class SqlInjectionTests(unittest.TestCase):
    def setUp(self):
        handle, self.path = tempfile.mkstemp(suffix=".sqlite3")
        os.close(handle)
        initialize(self.path)

    def tearDown(self):
        os.unlink(self.path)

    def test_demo_payload_exposes_only_synthetic_rows_in_vulnerable_example(self):
        self.assertEqual(len(vulnerable_search("' OR '1'='1", self.path)), 3)

    def test_same_payload_is_data_in_fixed_example(self):
        self.assertEqual(fixed_search("' OR '1'='1", self.path), [])


class ResilienceTests(unittest.TestCase):
    def test_offline_events_reconcile_once(self):
        edge = EdgeBuffer()
        cloud = CloudSink()
        event = {"device_id": "sensor_demo", "boot_id": "boot_demo", "seq": 1, "payload": {"level": 72}}
        edge.record(**event)
        edge.record(**event)
        self.assertEqual(len(edge.pending()), 1)
        self.assertEqual(reconcile(edge, cloud), 1)
        self.assertEqual(reconcile(edge, cloud), 1)
        self.assertEqual(edge.pending(), [])
        edge.close()


class DetectionTests(unittest.TestCase):
    def test_four_required_synthetic_detection_types(self):
        cases = [
            ({"type": "vpn_login", "hour": 2}, "vpn_anomalous_login"),
            ({"type": "http_request", "query": "' OR '1'='1"}, "sql_injection_pattern"),
            ({"type": "mqtt_connect", "certificate_valid": False}, "invalid_device_certificate"),
            ({"type": "actuator_command", "hour": 2, "profile": "unapproved"}, "actuator_out_of_profile"),
        ]
        for event, expected in cases:
            with self.subTest(expected=expected):
                self.assertIn(expected, detect(event))


if __name__ == "__main__":
    unittest.main()
