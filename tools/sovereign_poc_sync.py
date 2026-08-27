#!/usr/bin/env python3
"""Validate and stamp a Sovereign OS POC packet for backend handoff."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ONTOLOGY_NODE = "KOSPrime.SovereignOS"
ALLOWED_ACTION_TIERS = {"observe", "suggest", "draft", "execute"}
PROFILE_PATH = Path("config/sovereign-devpc.json")


def backend_revision() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def load_packet(path: Path) -> dict[str, Any]:
    try:
        packet = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"unable to read POC packet: {error}") from error
    if not isinstance(packet, dict):
        raise ValueError("POC packet must be a JSON object")
    if not isinstance(packet.get("intent"), str) or not packet["intent"].strip():
        raise ValueError("POC packet requires a non-empty intent")
    if not isinstance(packet.get("payload", {}), dict):
        raise ValueError("POC payload must be a JSON object")
    action_tier = packet.get("action_tier", "suggest")
    if action_tier not in ALLOWED_ACTION_TIERS:
        raise ValueError(f"unsupported action tier: {action_tier}")
    return packet


def create_sync_envelope(packet: dict[str, Any]) -> dict[str, Any]:
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    return {
        "bus": "PrimeBus",
        "packet_type": "lattice",
        "ontology_segment": ONTOLOGY_NODE,
        "intent": packet["intent"],
        "source": "SovereignOS.POC",
        "destination": packet.get("destination", "CognitiveEngine"),
        "correlation_id": packet.get("correlation_id"),
        "action_tier": packet.get("action_tier", profile["sovereignLayer"]["defaultActionTier"]),
        "backend_revision": backend_revision(),
        "dev_profile": profile["profileId"],
        "timestamp": time.time(),
        "payload": packet.get("payload", {}),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="POC JSON packet to synchronize")
    args = parser.parse_args()
    try:
        print(json.dumps(create_sync_envelope(load_packet(args.input))))
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"Sovereign POC sync error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())