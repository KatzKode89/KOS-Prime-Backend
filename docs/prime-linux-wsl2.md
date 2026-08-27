# Prime-Linux vOmega (WSL2 Ubuntu Node)

Prime-Linux vOmega is the Linux execution layer for KOS-Prime under Windows. It runs the Python Gemini/PrimeBus adapter and is reachable from Windows Copilot workflows through `wsl.exe`.

## Host setup

Run these commands from an elevated Windows PowerShell terminal, then restart if Windows requests it:

```powershell
wsl --install -d Ubuntu
```

Inside the Ubuntu distribution, initialize the execution environment:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip git
cd ~
git clone https://github.com/KatzKode89/KOS-Prime-Backend.git kos-prime
cd ~/kos-prime
```

The Ubuntu username determines the default path used by the Windows launcher. Pass `-LinuxRepoPath` when the repository is stored elsewhere.

## Windows-to-WSL invocation

From the repository checkout on Windows:

```powershell
.\windows-copilot\Invoke-KOSPrimeWsl.ps1 `
  -InputPath .\windows-copilot\sample-packet.json `
  -LinuxRepoPath "/home/your-ubuntu-user/kos-prime"
```

Inline packets are also supported:

```powershell
.\windows-copilot\Invoke-KOSPrimeWsl.ps1 `
  -Json '{"intent":"health.check","payload":{"module":"ShieldHullIntegrityArray","integrityPercentage":85}}' `
  -LinuxRepoPath "/home/your-ubuntu-user/kos-prime"
```

The launcher forwards stdin to `gemini_omni_agent.py` and preserves its JSON stdout response. Set `GEMINI_API_KEY` inside the WSL environment to enable live Gemini requests; with no key, the agent remains in local mock mode.

## Stack role

Prime-Linux vOmega is an execution node, not a replacement for PrimeBus. Windows/Copilot supplies commands, WSL2 runs the Python bridge, and the resulting packet remains governed by the `ShipCore_vOmega.Modules` ontology before downstream typed routing.