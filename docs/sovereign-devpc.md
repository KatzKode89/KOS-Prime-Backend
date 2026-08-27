# Sovereign OS Intel Core Ultra i9 Dev PC Profile

The `SovereignOS.IntelCoreUltraI9.DevPC` profile provides reproducible defaults for a Core Ultra i9-class development PC. It improves build and local adapter behavior without assuming a fixed CPU topology, changing firmware, overclocking, or controlling thermals.

## Apply the profile

From the repository root in PowerShell:

```powershell
$env:DOTNET_gcServer = "1"
$env:DOTNET_Thread_UseAllCpuGroups = "1"
$env:PYTHONUNBUFFERED = "1"
dotnet test KOSPrime.slnx --configuration Release
```

The same environment variables can be set in a Windows Terminal profile or CI job. Python worker counts should be derived at runtime rather than fixed to a guessed i9 core count.

## Sovereign Layer POC sync

The local sync adapter stamps a POC packet with the backend revision, dev profile, correlation ID, ontology node, and action tier:

```powershell
python3 tools/sovereign_poc_sync.py config/sovereign-poc-packet.json
```

The emitted packet is a handoff contract, not a network publish. A later service can submit it to PrimeBus after adapting the Sovereign OS envelope to the C# `PacketEnvelope` source, destination, type, and sequence fields.

## Boundaries

- `KOSPrime.SovereignOS` is the composition layer for the POC.
- PrimeBus remains the backend ontology router.
- The sync tool performs validation and stamping only; it does not execute actions.
- `execute` packets still require the multimodal governance confirmation rules.
- API keys and device-specific paths remain environment-only.