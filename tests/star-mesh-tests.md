# STAR-MESH Test Matrix

The daemon is a transport boundary. These checks must pass before connecting it to a live PrimeBus ingress.

| Scenario | Expected behavior |
| --- | --- |
| Malformed configuration | Reject startup with an error and nonzero exit code. |
| Unsupported configuration version | Reject startup with an error and nonzero exit code. |
| Invalid WebSocket endpoint | Reject startup with an error and nonzero exit code. |
| Unknown peer identity | Warn and continue; do not create an implicit route. |
| Invalid `packet_type` | Drop when `drop_unknown` is `true`; forward only when explicitly allowed by policy. |
| Malformed JSON message | Drop and log; keep the peer connection available. |
| Non-object JSON message | Drop and log; keep the peer connection available. |
| Queue limit | Apply the configured `transport.max_queue` bound. |
| Retry policy | Use peer `retry_ms`, `max_retries`, and transport backoff for future outbound connections. |
| Heartbeat | Use `transport.heartbeat_ms` for WebSocket liveness. |
| Health reporting | Emit node health on the configured `node.health_interval_ms`. |

The current skeleton implements configuration validation, packet-type filtering, malformed-message handling, and the inbound WebSocket boundary. Outbound peer retry, heartbeat telemetry, and PrimeBus publication remain explicit integration points rather than hidden behavior.