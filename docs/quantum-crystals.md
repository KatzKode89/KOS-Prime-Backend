# Quantum Crystals

QuantumCrystals provides the resonance and lattice state model used by the CrystalSeekers ship core. Its five internal modules are the Crystal-Core Resonance Chamber, Harmonic Phase Stabilizer, Dimensional Navigation Matrix, Inertial Dampening Grid, and Shield & Hull Integrity Array.

The lattice contract defines module identity, schema version, sequence, timestamp, state, correlation, and payload fields. The state machine is shared across the module group, with `Degraded` and `Faulted` states providing operational visibility without changing the module inventory.

Shield & Hull Integrity Array health checks monitor spatial shear, gravitational strain, resonance-dampening efficacy, and threshold status. Health and telemetry packets are routed through PrimeBus and persisted by ReclusionMemory for event correlation.