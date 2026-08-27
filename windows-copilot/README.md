# Windows Copilot Stack

This folder provides the Windows PowerShell entrypoint for the KOS-Prime Gemini/PrimeBus adapter. It is designed for use from Microsoft Windows Copilot workflows, Copilot Studio actions, or a local PowerShell terminal.

## Requirements

- Windows PowerShell 5.1 or PowerShell 7+
- Python 3.10+
- The repository checked out locally

No API key is needed for local mock mode. Set `GEMINI_API_KEY` in the process environment to enable the live Gemini request path. Use `GEMINI_MODEL` to select a model.

## Run a packet file

From the repository root:

```powershell
.\windows-copilot\Invoke-KOSPrimeCopilot.ps1 -InputPath .\windows-copilot\sample-packet.json
```

If script execution is restricted for the current process, use:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\windows-copilot\Invoke-KOSPrimeCopilot.ps1 -InputPath .\windows-copilot\sample-packet.json
```

## Run inline JSON

```powershell
.\windows-copilot\Invoke-KOSPrimeCopilot.ps1 -Json '{"intent":"health.check","payload":{"module":"ShieldHullIntegrityArray","integrityPercentage":85}}'
```

The launcher writes the agent's JSON response to standard output, making it suitable for capture by another Windows workflow. Errors are written to standard error and preserve a nonzero exit code.

## Edge Copilot handoff

Use `Invoke-KOSPrimeEdgeCopilot.ps1` when Microsoft Edge is the final human-facing Copilot surface:

```powershell
.\windows-copilot\Invoke-KOSPrimeEdgeCopilot.ps1 `
	-InputPath .\windows-copilot\sample-packet.json `
	-OutputPath .\kos-prime-edge-handoff.json `
	-OpenEdge
```

Add `-UseWsl -LinuxRepoPath "/home/your-ubuntu-user/kos-prime"` to execute through the WSL2 launcher. The script saves the PrimeBus-compatible JSON response and opens `https://copilot.microsoft.com/` in Edge. It does not inject text into the browser or automate Copilot chat input; the handoff file is the explicit boundary for review or a later approved workflow.