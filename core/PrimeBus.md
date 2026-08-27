# PrimeBus

## Ship core lattice routing

All Core Internal Module packets use the ontology segment `ShipCore_vOmega.Modules` and packet type `lattice`. PrimeBus is the sole communication boundary between TCJH, STAR-MESH, sensors, the tri-node backbone, and the ship core modules.

### Flow

1. TCJH, STAR-MESH, and sensors publish validated input packets.
2. CognitiveEngine consumes inputs and publishes module commands and control state.
3. The addressed module publishes state and output packets.
4. GenesisOutput consumes energy, navigation, and shield-related outputs.
5. ReclusionMemory consumes telemetry and health packets for persistence and event correlation.

### Routing contract

| Packet | Producer | Consumers |
| --- | --- | --- |
| `module.command` | CognitiveEngine | addressed Core Internal Module |
| `module.state` | Core Internal Module | CognitiveEngine, GenesisOutput when applicable |
| `module.telemetry` | Core Internal Module | ReclusionMemory |
| `module.health` | Core Internal Module | CognitiveEngine, ReclusionMemory |

Packets must include `sequence`, `timestamp`, `moduleName`, and `correlationId` when they participate in a multi-stage control cycle. Consumers must reject an unknown module identifier or an older sequence for the same module.