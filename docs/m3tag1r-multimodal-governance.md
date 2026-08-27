# M3t@G1r! Multimodal Agentic-Layer Governance

Version: `1.0.0`

This contract defines M3t@G1r! as a governed multimodal agentic layer for KOS-Prime. It coordinates camera-derived attention signals, voice and sound synthesis, and bounded agent actions through PrimeBus. It does not define a sentient entity, continuous surveillance system, or unrestricted autonomous operator.

## Modalities

| Modality | Input | Output | Default |
| --- | --- | --- | --- |
| Camera | Opt-in visual attention signal | `visual_attention` metadata only | Disabled |
| Voice | User-approved microphone input or text | `voice.lattice` synthesis packet | Disabled until enabled |
| Sound | System state, scene, or user-approved control | `sound.lattice` packet | Off until requested |
| Agentic action | Intent and validated context | Proposal, draft, or confirmed action | Proposal only |

## Camera and eye-contact policy

“Eye contact” is implemented as a low-resolution, local **visual-attention estimate**, not identity recognition. The camera adapter may report whether a face appears directed toward the interaction surface and a confidence value. It must not infer identity, demographics, mood, health, or protected attributes.

The adapter must:

- require explicit user opt-in for every session and expose an active-camera indicator;
- process frames locally where possible and emit metadata rather than images or video;
- discard frames immediately after feature extraction;
- provide pause, revoke, and shutdown controls that take effect immediately;
- default to `unknown` when confidence is below the configured threshold;
- never use visual attention to authorize an agentic action or infer consent.

Example metadata payload:

```json
{
  "visual_attention": "directed",
  "confidence": 0.82,
  "source": "local_camera",
  "frame_retained": false
}
```

## Voice and sound policy

Voice and sound use the existing `SynthStack_vOmega.Voice` and `SynthStack_vOmega.Sound` contracts. M3t@G1r! may select a voice profile and prosody only within the active PersonalityPolicy and user settings.

- Microphone capture requires explicit permission and a visible active state.
- Voice playback must identify itself as synthetic when context could cause confusion.
- Sound effects must not imitate emergency, authority, or safety-critical signals without an explicit application contract.
- Voice and sound may be muted independently of text responses.
- Audio artifacts and transcripts follow explicit retention settings; no raw recording is retained by default.

## Agentic action tiers

Every proposed action is classified before execution:

1. **Observe**: read permitted context and produce analysis.
2. **Suggest**: present a recommendation without changing state.
3. **Draft**: prepare a file, packet, or command for review.
4. **Execute**: perform an external or state-changing operation only after the required confirmation.

Camera attention, EmotionState, voice tone, or personality traits must never substitute for confirmation. Destructive, external, credentialed, financial, or privacy-sensitive actions always require explicit user confirmation at execution time.

## PrimeBus contracts

The governance layer uses these packet segments:

| Packet | Type | Purpose |
| --- | --- | --- |
| `KOSPrime.M3tG1r.VisualAttention` | `xr-frame` | Local, ephemeral attention metadata with confidence and consent state. |
| `KOSPrime.Emotion.State` | `lattice` | Bounded modulation signals from EmotionCore. |
| `KOSPrime.Personality.Policy` | `lattice` or `xr-frame` | Stable response constraints. |
| `KOSPrime.M3tG1r.ActionProposal` | `lattice` | Inspectable action tier, rationale, required confirmation, and correlation ID. |
| `SynthStack_vOmega.Sound` | `lattice` | Governed sound synthesis request. |
| `SynthStack_vOmega.Voice` | `lattice` | Governed voice synthesis request. |

PrimeBus validates packet type, ontology segment, source, destination, sequence, and correlation ID. STAR-MESH may transport these packets but does not authorize actions or interpret consent.

## Governance state

```text
Disabled -> OptedIn -> Active
Active -> Paused
Paused -> Active
OptedIn -> Revoked
Active -> Revoked
Active -> Disabled
```

Revocation terminates camera and microphone processing, cancels pending synthesis, and prevents execution of unconfirmed actions. The state transition and reason are logged as metadata without storing raw sensory input.

## Audit requirements

Each multimodal decision records the policy version, consent state, modality, correlation ID, action tier, and outcome. The audit trail must make it possible to answer what signal and policy produced an output without retaining raw camera frames, audio recordings, or unnecessary user text.