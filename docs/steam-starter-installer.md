# K@tz-0$-St3@m-St@rt3r PC Installer

The Windows installer is [Install-KatzStarterSteam.ps1](../windows-copilot/Install-KatzStarterSteam.ps1). It installs a completed Unity Windows x64 player for the CrystalSeekers: Echoes of Destiny starter demo into the current user's `%LOCALAPPDATA%\KatzStarterForSteam` directory.

## Build input

The installer expects a Unity build folder containing:

```text
builds/steam-windows-x64/
  KatzStarterForSteam.exe
  KatzStarterForSteam_Data/
  crystalseekers-steam-beta.json (optional)
```

The source package in this repository is not itself a playable Windows installer. Build the Unity project on a Windows or Unity-capable CI host first.

## Install and run

From PowerShell on Windows:

```powershell
.\windows-copilot\Install-KatzStarterSteam.ps1 -CreateDesktopShortcut -Launch
```

For a different build location:

```powershell
.\windows-copilot\Install-KatzStarterSteam.ps1 `
  -SourcePath "C:\Builds\CrystalSeekers\Windows" `
  -CreateDesktopShortcut
```

The default install is per-user and does not require administrator privileges. The script validates the optional product manifest and refuses a package that is not the fake-local starter profile.

## Product boundaries

This installer is for the small Steam starter demo only. The installed demo has no KOS-Prime backend, PrimeBus runtime, WSL2, Gemini, network service, camera, microphone, or real audio synthesis. Steamworks App ID, depot upload, store metadata, and signing remain publisher-managed.