# KOS-Prime Modules

The module specifications live under `modules/` and are designed to remain independently understandable.

- **ChaosField**: entropy and chaos simulation concepts.
- **ReclusionCore**: memory and isolation logic.
- **GenesisPulse**: creation and expansion logic.
- **NaniteMesh**: neural mesh communication, documented separately as a protocol and a specification.
- **QuantumCrystals**: lattice behavior and a state-machine model for crystal state transitions.

When proposing implementation work, define the module contract and its ontology messages before introducing cross-module dependencies. PrimeBus should remain the communication boundary.