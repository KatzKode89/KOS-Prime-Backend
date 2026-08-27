# Ontology

## `ShipCore_vOmega.Modules`

The `lattice` packet segment for CrystalSeekers ship core modules. This segment contains the shared vocabulary for module inputs, outputs, state, telemetry, and health events.

## `KOSPrime.StackArchitectureMap`

Versioned architecture-map node for the Windows/Copilot entrypoints, PowerShell-to-Python bridge, PrimeBus routing engine, QuantumCrystals, ChaosField, and tri-node backbone. The canonical visual and packet mapping is maintained in `docs/stack-architecture-map.md`.

## `SynthStack_vOmega.Sound`

The `lattice` packet segment for instrument, texture, environmental, and engine sound synthesis. Its packet contract is maintained in `docs/synthesizer-stack.md`.

## `SynthStack_vOmega.Voice`

The `lattice` packet segment for text-to-voice synthesis, voice profiles, prosody, emotion, and XR acoustic context. Its packet contract is maintained in `docs/synthesizer-stack.md`.

## `KOSPrime.KatzStarterModel`

Versioned baseline profile composing the Windows/Copilot entrypoints, Prime-Linux vOmega, Gemini adapter, STAR-MESH transport, PrimeBus router, core domains, tri-node backbone, and Synthesizer Stack contracts. The human-readable model is maintained in `docs/katz-starter-model.md` and the machine-readable profile in `docs/katz-starter-model.json`.

## `KOSPrime.Emotion.State`

Versioned `lattice` packet for bounded EmotionCore policy signals: mood, energy, focus, and tension. The state is observable, clamped, smoothed, and logged; it is not a claim of subjective experience.

## `KOSPrime.Personality.Policy`

Versioned `lattice` or `xr-frame` packet containing deterministic response constraints derived from a trait profile, role contract, and EmotionState. The contract is maintained in `docs/emotional-processor-personality.md`.

## `KOSPrime.M3tG1r.Persona`

Governed synthetic persona façade composed of EmotionCore, PersonalityPolicy, CognitiveEngine, and GenesisOutput. It expresses a versioned role contract through PrimeBus packets and makes no claim of subjective emotion or autonomous identity. The canonical definition is maintained in `docs/m3tag1r-persona.md`.

## `KOSPrime.M3tG1r.MultimodalGovernance`

Versioned governance contract for M3t@G1r! camera-derived visual-attention metadata, Synthesizer Stack voice/sound packets, and bounded agentic action tiers. Camera and microphone access are opt-in, raw sensory data is not retained by default, and visual attention never authorizes an action. The contract is maintained in `docs/m3tag1r-multimodal-governance.md`.

## `KOSPrime.SovereignOS`

Top-level governed cognitive-stack composition for PrimeBus, the tri-node backbone, M3t@G1r!, EmotionCore, PersonalityPolicy, SynthStack, and multimodal governance. The canonical model is maintained in `docs/sovereign-os.md`.

## `KOSPrime.GlyphSystem`

Versioned visual-token annotation layer for lattice, chaos, resonance, persona, and governance cues. Glyphs are non-linguistic, non-identity-bearing, non-emotional, and cannot authorize actions. The specification is maintained in `docs/glyph-system/` and the family registries in `core/glyphs/`.

## `KOSPrime.Katz0sWSL2`

Versioned Windows Subsystem for Linux 2 execution profile for the Prime-Linux vOmega node. It defines the Ubuntu toolchain, Windows-to-WSL launcher path, and credential/privacy boundaries without introducing another router or module. The profile is maintained in `docs/katz-0s-wsl2.md` and `docs/katz-0s-wsl2.json`.

### Ownership

- **CognitiveEngine** interprets intent, computes control state, and monitors module integrity.
- **ReclusionMemory** persists telemetry, phase history, inertia events, and correlated health traces.
- **GenesisOutput** synthesizes energy vectors, navigation feeds, shield harmonics, and final telemetry outputs.

### Packet vocabulary

- `lattice`: crystal resonance, phase, spatial, inertial, and structural state packets.
- `module.command`: control input addressed to one Core Internal Module.
- `module.state`: current state and measured output from a Core Internal Module.
- `module.telemetry`: persistent observation for ReclusionMemory.
- `module.health`: health status, thresholds, and fault information.

### Semantic boundaries

The five predefined modules are the complete Core Internal Modules list. New behavior must extend an existing module contract or a separate ontology segment; it must not silently create another Core Internal Module.