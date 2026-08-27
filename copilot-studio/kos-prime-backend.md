# KOS-Prime Backend Overview

KOS-Prime is a modular backend and simulation architecture. Its shared foundation is under `core/`, startup documentation is under `init/`, domain nodes are under `nodes/`, feature modules are under `modules/`, and architectural references are under `docs/`.

The current repository is a specification scaffold. It documents the intended architecture but does not yet provide executable backend services or Unity runtime implementations.

## Core Concepts

- PrimeBus is the intended routing layer between nodes and modules.
- Ontology documents define shared domain vocabulary and packet types.
- The tri-node backbone consists of CognitiveEngine, ReclusionMemory, and GenesisOutput.
- Unity runtime integration is an intended consumer of the backend contracts.