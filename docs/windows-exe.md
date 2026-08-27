# Windows EXE Build and Install

The repository includes `KOSPrime.Runner`, a small Windows console host for the existing PrimeBus and ShieldHullIntegrityArray runtime path.

## Build on Windows or Codespaces

From the repository root:

```powershell
dotnet publish .\src\KOSPrime.Runner\KOSPrime.Runner.csproj `
  --configuration Release `
  --runtime win-x64 `
  --self-contained false `
  --output .\publish\win-x64
```

This produces `publish\win-x64\KOSPrime.Runner.exe`. The target machine must have the matching .NET 9 runtime installed when using `--self-contained false`.

For a standalone EXE that carries the runtime, replace `--self-contained false` with `--self-contained true`. That output is larger and should be distributed separately rather than committed to Git.

## Install on Windows

Run from PowerShell after publishing:

```powershell
.\windows-copilot\Install-KOSPrime.ps1 -AddToUserPath
```

The installer copies the published files to `%LOCALAPPDATA%\KOS-Prime\bin` and optionally adds that directory to the user PATH. No administrator privileges are required for the default install location.

## Run

```powershell
KOSPrime.Runner.exe --health 85
```

The runner emits JSON containing the route result and the `ShipCore_vOmega.Modules` health packet. This is a runtime smoke host, not a Windows service or background daemon.