# Ontology

## `ShipCore_vOmega.Modules`

The `lattice` packet segment for CrystalSeekers ship core modules. This segment contains the shared vocabulary for module inputs, outputs, state, telemetry, and health events.

## `KOSPrime.StackArchitectureMap`

Versioned architecture-map node for the Windows/Copilot entrypoints, PowerShell-to-Python bridge, PrimeBus routing engine, QuantumCrystals, ChaosField, and tri-node backbone. The canonical visual and packet mapping is maintained in `docs/stack-architecture-map.md`.

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