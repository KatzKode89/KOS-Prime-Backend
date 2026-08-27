# PersonalityPolicy

## Stable Response Policy

PersonalityPolicy maps a versioned trait profile, role contract, and current `EmotionState` into explicit response constraints. It shapes behavior; it does not create an autonomous identity or override safety and system policies.

### Trait profile

Traits are normalized to `[0.0, 1.0]` and loaded from `trait-profile.json`:

- `Openness`
- `Warmth`
- `Directness`
- `Playfulness`
- `Precision`

Roles are explicit, versioned contracts such as `sovereign_os_companion`, `architect`, and `coach`.

### Policy output

The policy engine combines traits, role, and bounded EmotionState to select a response mode, such as `calm-technical`, `gentle-brief`, or `playful-structured`. It emits a `KOSPrime.Personality.Policy` packet using `lattice` or `xr-frame` when an XR surface is involved.

The packet must include:

- `policyVersion` and `role`.
- `responseMode`.
- `maxLength`.
- `tone` and allowed topic depth.
- `challengeIntensity`.
- Trait and emotion input references, without storing raw user text unnecessarily.

PersonalityPolicy must remain deterministic for the same profile, role, emotion state, and policy version. CognitiveEngine consumes the policy for planning; GenesisOutput applies formatting constraints.