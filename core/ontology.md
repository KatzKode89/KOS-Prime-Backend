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