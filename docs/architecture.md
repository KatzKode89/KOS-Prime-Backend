# Architecture Overview

## CrystalSeekers ship core

The CrystalSeekers ship core is represented by five predefined internal modules in the QuantumCrystals lattice domain. They share the `ShipCore_vOmega.Modules` ontology segment and communicate through PrimeBus.

The tri-node backbone remains the ownership model:

- CognitiveEngine interprets intent, computes control state, and monitors integrity.
- ReclusionMemory logs and recalls telemetry, state transitions, phase history, and inertia events.
- GenesisOutput generates energy vectors, navigation feeds, shield modulation, and final telemetry outputs.

There are no direct module-to-module links. Module commands, state, telemetry, and health events use the PrimeBus contract defined in `core/PrimeBus.md`.

See [KOSPrime.StackArchitectureMap](stack-architecture-map.md) for the complete entrypoint, routing, packet, and tri-node flow map.