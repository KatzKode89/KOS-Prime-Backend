# KOS-Prime Copilot Instructions

## Project Overview

KOS-Prime is a modular backend and simulation architecture for a cosmic simulation engine. The repository currently contains Markdown specifications and architecture placeholders for PrimeBus routing, ontology definitions, a tri-node backbone, NaniteMesh networking, QuantumCrystals, and Unity runtime integration.

## Repository Structure

- `core/`: PrimeBus, ontology, and shared type definitions.
- `init/`: startup and boot-sequence documentation.
- `nodes/`: CognitiveEngine, ReclusionMemory, and GenesisOutput nodes.
- `modules/`: ChaosField, ReclusionCore, GenesisPulse, NaniteMesh, and QuantumCrystals.
- `docs/`: architecture and domain reference material.

## Design Rules

- Keep modules isolated and communicate through PrimeBus contracts.
- Define shared packet and domain types through the ontology before adding consumers.
- Preserve the separation between NaniteMesh protocol and specification documents.
- Model QuantumCrystals as a state-machine-driven lattice subsystem.
- Keep the tri-node backbone explicit: CognitiveEngine, ReclusionMemory, and GenesisOutput.
- Prefer C# for Unity runtime code and Markdown for backend specifications unless an existing convention requires otherwise.

## Change Guidance

- Inspect nearby specifications before adding a new module or type.
- Use the existing folder and naming conventions; use lowercase kebab-case for Markdown filenames.
- Avoid coupling modules directly to one another when a PrimeBus message or ontology type is appropriate.
- Update relevant documentation when changing architecture or message contracts.
- Do not claim that a subsystem is implemented when the repository only contains a specification placeholder.

## Validation

- Check links and filenames against the repository structure.
- Run `git diff --check` before committing documentation changes.
- Keep commits focused and use descriptive conventional commit messages.