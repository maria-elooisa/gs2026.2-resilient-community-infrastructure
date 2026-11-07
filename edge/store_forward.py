"""Small offline-first edge queue used to demonstrate WAN loss and replay."""

import json
import sqlite3


class EdgeBuffer:
    def __init__(self, path=":memory:"):
        self.connection = sqlite3.connect(path)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS events "
            "(device_id TEXT, boot_id TEXT, seq INTEGER, payload TEXT, sent INTEGER DEFAULT 0, "
            "PRIMARY KEY(device_id, boot_id, seq))"
        )
        self.connection.commit()

    def record(self, device_id, boot_id, seq, payload):
        self.connection.execute(
            "INSERT OR IGNORE INTO events(device_id, boot_id, seq, payload) VALUES (?, ?, ?, ?)",
            (device_id, boot_id, seq, json.dumps(payload, sort_keys=True)),
        )
        self.connection.commit()

    def pending(self):
        rows = self.connection.execute(
            "SELECT device_id, boot_id, seq, payload FROM events WHERE sent=0 ORDER BY device_id, boot_id, seq"
        ).fetchall()
        return [dict(device_id=r[0], boot_id=r[1], seq=r[2], payload=json.loads(r[3])) for r in rows]

    def acknowledge(self, device_id, boot_id, seq):
        self.connection.execute(
            "UPDATE events SET sent=1 WHERE device_id=? AND boot_id=? AND seq=?",
            (device_id, boot_id, seq),
        )
        self.connection.commit()

    def close(self):
        self.connection.close()


class CloudSink:
    """Idempotent receiver keyed by device, boot and monotonic sequence."""

    def __init__(self):
        self.received = {}

    def ingest(self, event):
        key = (event["device_id"], event["boot_id"], event["seq"])
        self.received.setdefault(key, event["payload"])


def reconcile(edge, cloud):
    for event in edge.pending():
        cloud.ingest(event)
        edge.acknowledge(event["device_id"], event["boot_id"], event["seq"])
    return len(cloud.received)
