# K@tz-0$-Pr1m3-GU1

Version: `1.0.0`

`K@tz-0$-Pr1m3-GU1` is the governed operator GUI layer for Sovereign OS. It provides a desktop-first control and observability surface over the existing Windows overlay, Unity cockpit, PrimeBus, Glyph System, SynthStack, STAR-MESH, and tri-node contracts.

It is a presentation and intent layer, not a replacement for PrimeBus and not an unrestricted control console.

## Screen model

| Region | Primary content | Default access |
| --- | --- | --- |
| Status rail | Connection state, system integrity, policy version, consent indicators | Read-only |
| ShipCore panel | Health, lattice state, QuantumCrystals, and ShieldHullIntegrityArray status | Read-only |
| STAR-MESH map | Node status, peer latency, and transport events | Read-only; selection creates a proposal |
| Council feed | CognitiveEngine, ReclusionMemory, and GenesisOutput correlated events | Read-only |
| Glyph canvas | Validated glyph annotations and governance cues | Read-only |
| SynthStack deck | Active voice profile, instrument, sound context, and mute controls | Mute is local; synthesis requests are proposals |
| Action drawer | Observe, suggest, draft, and execute proposals with confirmation state | Confirmation-gated |

## Packet binding

The GUI consumes the Windows overlay contract and never binds raw transport data directly to controls.

| Packet | View-model target |
| --- | --- |
| `state` / `module.health` | `ShipCoreStatus`, `SystemIntegrity` |
| `star-mesh` | `StarMeshNodeStatus`, `CrossNodeLatency` |
| `synthstack.voice` | `ActiveVoiceProfile` |
| `synthstack.sound` | `CurrentInstrument`, `SoundContext` |
| `glyph.annotation` | `ActiveGlyphs` |
| `council` | `CouncilState` |
| `KOSPrime.M3tG1r.ActionProposal` | `PendingAction`, `ConfirmationState` |

Every displayed event retains its `correlation_id`, source, timestamp, and sequence metadata for diagnostics. Unknown packet types are ignored and surfaced only as a non-authoritative diagnostic.

## Interaction governance

The GUI action flow is:

```text
observe -> suggest -> draft -> confirm -> execute
```

Camera attention, glyphs, EmotionState, voice tone, and personality traits cannot advance an action through `confirm`. Destructive, external, credentialed, and privacy-sensitive operations require explicit user confirmation at the point of execution. The GUI must show the action tier and confirmation state before presenting an execute control.

## Visual and accessibility rules

- Use text and icon-plus-text labels for critical state; glyphs are supplemental.
- Provide keyboard navigation, screen-reader names, focus indicators, and non-color status representations.
- Keep connection, consent, mute, and confirmation indicators persistently visible.
- Do not display raw camera frames, microphone content, API keys, or secret paths.
- Render disconnected state as `Disconnected`; do not substitute synthetic subsystem values.
- Support independent text, voice, and sound mute controls.

## Runtime binding

The implementation may target WinUI/WPF or Unity desktop/XR, but the client must use the corresponding `PrimeBusClient` or Unity bridge adapter. UI state updates occur on the UI thread, subscriptions are disposed when the view closes, and PrimeBus remains responsible for packet validation and routing.

## Ontology

The canonical node is `KOSPrime.SovereignOS.GUI`. It composes the existing `KOSPrime.SovereignOS.WindowsOverlay`, `KOSPrime.SovereignOS.UnityCockpit`, and `KOSPrime.M3tG1r.MultimodalGovernance` contracts.