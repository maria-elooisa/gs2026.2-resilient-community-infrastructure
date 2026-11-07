"""Create a hash manifest and custody record for the synthetic incident fixture."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "forensics" / "incident_events.jsonl"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--collector", required=True, help="fictional team member responsible for this lab collection")
    parser.add_argument("--location", required=True, help="lab machine or synthetic evidence location")
    parser.add_argument("--method", default="SHA-256 of the immutable synthetic JSONL fixture")
    args = parser.parse_args()
    content = SOURCE.read_bytes()
    record = {
        "evidence_id": "EVID-SYNTH-001",
        "source_file": "forensics/incident_events.jsonl",
        "sha256": hashlib.sha256(content).hexdigest(),
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "collector": args.collector,
        "location": args.location,
        "method": args.method,
        "synthetic_data": True,
    }
    output = ROOT / "artifacts"
    output.mkdir(exist_ok=True)
    destination = output / "custody_manifest.json"
    destination.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Manifesto criado: {destination}")
    print(f"SHA-256: {record['sha256']}")


if __name__ == "__main__":
    main()
