# Windows Sovereign OS Overlay Contract

Version: `1.0.0`

This document defines the contract for a future WinUI/WPF overlay that presents KOS-Prime state. The repository currently does not contain a native Windows overlay implementation; `PrimeBusClient`, `OverlayViewModel`, and `OverlayWindow` remain client-side integration points.

## Layers

| Layer | Responsibility |
| --- | --- |
| `PrimeBusClient` | Connect to the optional `KOSPrimeBusPipe`, read newline-delimited JSON, validate packets, and dispatch parsed updates. |
| `OverlayViewModel` | Own bindable state and collections; never make routing decisions. |
| `OverlayWindow` | Render XAML controls and expose accessible status/fallback indicators. |
| Fallback heartbeat | Show bounded connection health only when the pipe is unavailable; never invent ship or user state. |

## Packet binding map

| Packet type | Payload fields | Overlay target |
| --- | --- | --- |
| `state` | `Status`, `IntegrityPercentage` | `ShipCoreStatus`, `SystemIntegrity` |
| `star-mesh` | `NodeStatus`, `LatencyMs` | `StarMeshNodeStatus`, `CrossNodeLatency` |
| `synthstack.voice` | `VoiceProfileId` | `ActiveVoiceProfile` |
| `synthstack.sound` | `InstrumentId` | `CurrentInstrument` |
| `glyph.annotation` | `glyph_id`, `family` | `ActiveGlyphs` collection |
| `council` | `TriNodeState` | `CouncilState` |

The client must preserve `correlation_id`, `timestamp`, and packet sequence metadata for diagnostics. It must ignore unknown packet types without crashing or presenting them as trusted state.

## Transport contract

The named pipe is an optional local presentation transport, not a replacement for PrimeBus. A future client should:

1. Connect to `KOSPrimeBusPipe` with an explicit timeout.
2. Read one JSON object per line.
3. Validate the packet envelope and ontology segment before binding fields.
4. Marshal view-model updates to the UI thread.
5. Dispose the pipe and subscriptions when the window closes.

When disconnected, the overlay may show `Disconnected` and a bounded heartbeat timestamp. It must not synthesize integrity, node, audio, glyph, council, or identity data.

## Governance

- The overlay is read-only unless a separate, confirmed command contract is introduced.
- Camera attention and glyph state never authorize commands.
- Audio profile and instrument fields are display metadata; they do not trigger playback by themselves.
- Raw camera frames, microphone data, and pipe contents are not retained by default.
- All UI updates remain subordinate to `KOSPrime.M3tG1r.MultimodalGovernance`.

## Client routing pseudocode

```text
switch packet.packet_type:
  state             -> UpdateShipCore(packet)
  star-mesh         -> UpdateStarMesh(packet)
  synthstack.voice  -> UpdateVoice(packet)
  synthstack.sound  -> UpdateSound(packet)
  glyph.annotation  -> UpdateGlyphs(packet)
  council           -> UpdateCouncil(packet)
  otherwise         -> IgnoreUnknown(packet)
```