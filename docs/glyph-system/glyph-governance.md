# Glyph Governance and Rendering

Glyphs are annotations only. They may visualize a validated state or policy, but they never become a command, permission, identity marker, emotion claim, camera frame, audio sample, or autonomous trigger.

## Allowed behavior

- Signal attention, confirmation tier, or revocation state.
- Annotate PrimeBus packets after packet validation.
- Modulate a permitted persona response mode.
- Render as a Unity HUD, vector shape, shader overlay, or particle primitive.

## Prohibited behavior

- Encode identity, biometric information, or protected attributes.
- Encode or retain camera frames, audio samples, or raw user content.
- Authorize an action, replace explicit confirmation, or escalate an action tier.
- Imply subjective emotion or hidden intent.

## Packet rules

Glyph arrays must appear inside an existing PrimeBus packet with `packet_type`, `ontology_segment`, source, destination, timestamp, sequence, and correlation ID. Consumers must reject an unknown glyph, family/context mismatch, or governance requirement that is not satisfied by the parent packet.

Governance glyphs follow `KOSPrime.M3tG1r.MultimodalGovernance`. `execute-sigil` is a visual label for an already-confirmed execution state; it cannot cause execution. `revocation-mark` must render immediately when consent is revoked and must not be retained beyond the applicable audit policy.

## Rendering rules

Rendering is stateless and non-retentive. A renderer should use stable dimensions, accessible contrast, and a text or state fallback for users who cannot perceive the visual token. Unity implementation remains a future consumer of this contract.