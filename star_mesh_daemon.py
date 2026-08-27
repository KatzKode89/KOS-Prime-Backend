#!/usr/bin/env python3
"""STAR-MESH transport boundary for KOS-Prime.

This daemon validates WebSocket packets and emits accepted packets to stdout
for a future PrimeBus ingress process. It intentionally does not implement
PrimeBus routing or module dispatch.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import websockets


LOGGER = logging.getLogger("star-mesh")
PACKET_TYPES = {"entropy", "chaos", "expansion", "lattice", "xr-frame"}


def load_config(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as config_file:
            config = json.load(config_file)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Unable to load STAR-MESH config: {error}") from error

    if not isinstance(config, dict):
        raise ValueError("STAR-MESH config must be a JSON object")
    validate_config(config)
    return config


def validate_config(config: dict[str, Any]) -> None:
    if config.get("version") != "1.0.0":
        raise ValueError("Unsupported STAR-MESH config version")

    node = config.get("node")
    if not isinstance(node, dict) or not node.get("id") or node.get("role") != "transport":
        raise ValueError("node.id and node.role=transport are required")
    parse_endpoint(node.get("ws_endpoint"))

    packet = config.get("packet")
    if not isinstance(packet, dict):
        raise ValueError("packet configuration is required")
    allowed_types = packet.get("allowed_types")
    if not isinstance(allowed_types, list) or not allowed_types:
        raise ValueError("packet.allowed_types must be a non-empty list")
    if not set(allowed_types).issubset(PACKET_TYPES):
        raise ValueError("packet.allowed_types contains an unsupported packet type")
    if not isinstance(packet.get("drop_unknown"), bool):
        raise ValueError("packet.drop_unknown must be boolean")

    peers = config.get("peers", [])
    if not isinstance(peers, list):
        raise ValueError("peers must be a list")
    peer_ids: set[str] = set()
    for peer in peers:
        if not isinstance(peer, dict) or not peer.get("id") or peer["id"] in peer_ids:
            raise ValueError("each peer requires a unique id")
        parse_endpoint(peer.get("endpoint"))
        if not isinstance(peer.get("retry_ms"), int) or peer["retry_ms"] < 0:
            raise ValueError("peer.retry_ms must be a non-negative integer")
        if not isinstance(peer.get("max_retries"), int) or peer["max_retries"] < 0:
            raise ValueError("peer.max_retries must be a non-negative integer")
        peer_ids.add(peer["id"])

    transport = config.get("transport")
    if not isinstance(transport, dict):
        raise ValueError("transport configuration is required")
    for key in ("max_queue", "heartbeat_ms", "backoff_ms"):
        if not isinstance(transport.get(key), int) or transport[key] <= 0:
            raise ValueError(f"transport.{key} must be a positive integer")


def parse_endpoint(endpoint: Any) -> tuple[str, int]:
    if not isinstance(endpoint, str):
        raise ValueError("WebSocket endpoint must be a string")
    parsed = urlparse(endpoint)
    if parsed.scheme != "ws" or not parsed.hostname or parsed.port is None:
        raise ValueError(f"Invalid WebSocket endpoint: {endpoint}")
    return parsed.hostname, parsed.port


async def forward_to_primebus(packet: dict[str, Any]) -> None:
    """Emit accepted transport data for a future PrimeBus ingress adapter."""
    print(json.dumps(packet), flush=True)


def packet_is_allowed(packet: dict[str, Any], config: dict[str, Any]) -> bool:
    packet_type = packet.get("packet_type")
    allowed_types = set(config["packet"]["allowed_types"])
    if packet_type in allowed_types:
        return True
    LOGGER.warning("Dropping packet with unsupported packet_type=%r", packet_type)
    return not config["packet"]["drop_unknown"]


async def handle_peer(websocket: Any, config: dict[str, Any]) -> None:
    async for message in websocket:
        try:
            packet = json.loads(message)
        except json.JSONDecodeError:
            LOGGER.warning("Dropping malformed JSON packet")
            continue
        if not isinstance(packet, dict):
            LOGGER.warning("Dropping non-object packet")
            continue
        if packet_is_allowed(packet, config):
            await forward_to_primebus(packet)


async def run(config: dict[str, Any]) -> None:
    host, port = parse_endpoint(config["node"]["ws_endpoint"])
    LOGGER.info("Listening on ws://%s:%s", host, port)

    async def handler(websocket: Any) -> None:
        await handle_peer(websocket, config)

    async with websockets.serve(handler, host, port, max_queue=config["transport"]["max_queue"]):
        await asyncio.Future()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("star-mesh.json"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="[STAR-MESH] %(message)s")
    try:
        config = load_config(args.config)
        asyncio.run(run(config))
    except (ValueError, OSError) as error:
        LOGGER.error("%s", error)
        return 1
    except KeyboardInterrupt:
        LOGGER.info("Stopping")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())