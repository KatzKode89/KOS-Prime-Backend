#!/usr/bin/env python3
"""PrimeBus-aware Gemini adapter for KOS-Prime.

The adapter reads one JSON packet from stdin and writes one JSON response packet
to stdout. Without GEMINI_API_KEY it runs in deterministic mock mode, which
makes local pipelines safe to exercise without external setup.
"""

from __future__ import annotations

import json
import os
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent"
)
ONTOLOGY_SEGMENT = "ShipCore_vOmega.Modules"


def make_primebus_packet(intent: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Wrap an agent result in the shared KOS-Prime packet shape."""
    return {
        "bus": "PrimeBus",
        "packet_type": "lattice",
        "ontology_segment": ONTOLOGY_SEGMENT,
        "intent": intent,
        "payload": payload,
        "timestamp": time.time(),
    }


def _mock_gemini(prompt: str, context: dict[str, Any]) -> dict[str, Any]:
    return {
        "gemini_model": GEMINI_MODEL,
        "mode": "mock",
        "prompt": prompt,
        "context": context,
        "response": {
            "summary": "Mock Gemini response aligned with KOS-Prime ontology.",
            "modules": [
                "ChaosField",
                "ReclusionCore",
                "GenesisPulse",
                "NaniteMesh",
                "QuantumCrystals",
            ],
            "routing": {
                "producer": "GeminiOmniAgent",
                "consumer": "CognitiveEngine",
                "primebus_channel": ONTOLOGY_SEGMENT,
            },
        },
    }


def call_gemini(prompt: str, context: dict[str, Any]) -> dict[str, Any]:
    """Call Gemini when configured, otherwise return a local mock response."""
    if not GEMINI_API_KEY:
        return _mock_gemini(prompt, context)

    request_body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"},
    }
    request = Request(
        GEMINI_ENDPOINT.format(model=GEMINI_MODEL),
        data=json.dumps(request_body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY,
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=60) as response:
            result = json.load(response)
    except (HTTPError, URLError, TimeoutError) as error:
        raise RuntimeError(f"Gemini request failed: {error}") from error

    try:
        text = result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("Gemini returned an unexpected response shape") from error

    try:
        structured_response: Any = json.loads(text)
    except json.JSONDecodeError:
        structured_response = {"text": text}

    return {
        "gemini_model": GEMINI_MODEL,
        "mode": "live",
        "response": structured_response,
        "context": context,
    }


def build_prompt(intent: str, payload: dict[str, Any]) -> str:
    return (
        "You are Gemini operating inside the KOS-Prime Engine.\n"
        f"Intent: {intent}\n"
        f"Payload: {json.dumps(payload, sort_keys=True)}\n\n"
        "Respond with structured, implementation-ready specifications, routing "
        "contracts, and module-aligned outputs that fit the existing KOS-Prime "
        "ontology. Do not invent new modules or runtime code."
    )


def main() -> int:
    if sys.stdin.isatty():
        print(
            "Gemini Omni Agent: expecting a JSON packet on stdin.",
            file=sys.stderr,
        )
        return 1

    try:
        incoming = json.load(sys.stdin)
        if not isinstance(incoming, dict):
            raise ValueError("input packet must be a JSON object")
        intent = str(incoming.get("intent", "unknown"))
        payload = incoming.get("payload", {})
        if not isinstance(payload, dict):
            raise ValueError("packet payload must be a JSON object")
        result = call_gemini(
            build_prompt(intent, payload),
            context={"katzos_packet": incoming},
        )
        print(json.dumps(make_primebus_packet("gemini.omni.response", result)))
        return 0
    except (json.JSONDecodeError, ValueError, RuntimeError) as error:
        print(f"Gemini Omni Agent error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())