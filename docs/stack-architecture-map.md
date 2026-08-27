# KOSPrime.StackArchitectureMap

Packet type: `lattice`

This document is the versioned architecture blueprint for the KOS-Prime stack. It describes the current implementation boundary and the intended flow between Windows/Copilot entrypoints, the PrimeBus routing engine, QuantumCrystals, ChaosField, and the tri-node backbone.

## Architecture Map

```mermaid
flowchart LR
    subgraph Entry[Entrypoint Layer]
        Win[Windows Copilot]
        PS[PowerShell launcher]
        Py[gemini_omni_agent.py]
        WSL[Prime-Linux vOmega / WSL2 Ubuntu]
        Events[TCJH / STAR-MESH / sensors]
        Win --> PS
        PS -->|JSON stdin/stdout| WSL --> Py
    end

    subgraph Bus[PrimeBus Routing Engine]
        Ont[ShipCore_vOmega.Modules ontology]
        Route[IPrimeBus / PrimeBus]
        Classify[Packet classification and sequence validation]
        Ont --> Route --> Classify
    end

    subgraph Core[Core Module Layer]
        QC[QuantumCrystals]
        Chaos[ChaosField]
        Cognitive[CognitiveEngine]
        Memory[ReclusionMemory]
        Genesis[GenesisOutput]
    end

    PS -->|environment and commands| Route
    Py -->|lattice response packet| Route
    Events -->|entropy / chaos input| Route
    Classify --> QC
    Classify --> Chaos
    Classify --> Cognitive
    Classify --> Memory
    Classify --> Genesis
    QC -->|resonance and harmonic state| Genesis
    Chaos -->|entropy and unpredictability vectors| Cognitive
    Cognitive -->|commands and control state| Route
    Memory -->|recall and telemetry history| Cognitive
    Genesis -->|output vectors and telemetry| Route
```

PowerShell is an entrypoint adapter, not a second routing engine. It forwards JSON to the Python bridge directly or through Prime-Linux vOmega in WSL2; the C# PrimeBus remains the typed routing boundary.

## Layer Responsibilities

| Layer | Components | Responsibility |
| --- | --- | --- |
| Entrypoint | Windows Copilot, PowerShell, Prime-Linux vOmega, Python bridge | Ingest user commands and environment events, then provide Linux execution under Windows. |
| Routing | `IPrimeBus`, `PrimeBus`, ontology | Validate registered endpoints, classify packets, enforce sequence ordering, and dispatch. |
| Crystal domain | QuantumCrystals | Process lattice resonance, harmonic energy, and crystal state transitions. |
| Chaos domain | ChaosField | Evaluate entropy and chaos vectors from environment or command inputs. |
| Tri-node backbone | CognitiveEngine, ReclusionMemory, GenesisOutput | Compute control decisions, persist and recall history, and synthesize outputs and telemetry. |

## Packet Mapping

| Component | Packet types | Flow |
| --- | --- | --- |
| Entrypoints | `entropy`, `chaos` | Environment notifications and command ingestion. |
| PrimeBus | `expansion`, `lattice` | Context orchestration and modular dispatch. |
| QuantumCrystals | `lattice` | Resonance and harmonic-energy packets. |
| ChaosField | `entropy`, `chaos` | Entropy-vector processing and chaotic evaluation. |
| Tri-node backbone | `lattice`, `xr-frame` | Decisions, recall, synthesis, and telemetry. |

All executable C# packets use `PacketEnvelope` and the fields defined in `src/KOSPrime.Core/PacketTypes.cs`. The Python bridge emits a JSON envelope with `packet_type`, `ontology_segment`, and `intent`; it must be adapted to the C# source, destination, type, and sequence fields before direct bus publication.

## Integration Contracts

- Entrypoints submit packets through an adapter and do not call core modules directly.
- PrimeBus validates `ShipCore_vOmega.Modules`, registered source and destination modules, and monotonic source sequences.
- Core modules publish commands, state, telemetry, and health through PrimeBus.
- CognitiveEngine owns decision and runtime control logic.
- ReclusionMemory owns persistence, recall, and event correlation.
- GenesisOutput owns final control vectors, energy modulation, and telemetry emission.
- No new module is implied by this map; QuantumCrystals and ChaosField remain the documented core domains.
- Prime-Linux vOmega is an execution node under Windows, not a new KOS-Prime module or routing layer.

## Monitoring Path

GenesisOutput should attach a correlation identifier to synthesized outputs and telemetry so an entrypoint command can be traced through PrimeBus, module state, and final output. Health packets from ShieldHullIntegrityArray remain available to CognitiveEngine and ReclusionMemory for threshold monitoring and event history.

## Registration

The canonical ontology node is `KOSPrime.StackArchitectureMap`. Changes to layer ownership, packet mappings, or routing boundaries should update this document and the related ontology references together.