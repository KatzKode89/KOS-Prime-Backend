# KOS-Prime Architecture

## Tri-Node Backbone

The primary node topology is:

- **CognitiveEngine**: cognitive processing responsibilities.
- **ReclusionMemory**: memory and reclusion responsibilities.
- **GenesisOutput**: output and generation responsibilities.

PrimeBus is the intended routing boundary connecting nodes and modules. Ontology definitions provide the shared vocabulary for packets and routing rules. QuantumCrystals contributes lattice and state-machine concepts, including XR-frame output requirements documented by the core types.

## Extension Pattern

New capabilities should be introduced as an isolated module under `modules/`, described in Markdown first, and connected through explicit PrimeBus and ontology contracts. Architecture changes should be reflected in the relevant files under `docs/`.