# K@tz-0$-WSL2

Version: `1.0.0`

`K@tz-0$-WSL2` is the named Windows Subsystem for Linux 2 execution profile for the KOS-Prime stack. It is the host configuration for Prime-Linux vOmega, not a new ontology router or backend module.

## Role

- Run the Python Gemini and STAR-MESH adapters under Ubuntu.
- Provide a repeatable Linux toolchain for KOS-Prime development.
- Receive Windows/Copilot packets through the PowerShell WSL launcher.
- Keep PrimeBus as the typed ontology and dispatch boundary.

## Windows setup

From an elevated PowerShell terminal on Windows:

```powershell
wsl --install -d Ubuntu
```

After the requested restart, create the Ubuntu user and run:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip git
git clone https://github.com/KatzKode89/KOS-Prime-Backend.git ~/kos-prime
cd ~/kos-prime
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Launch profile

From a Windows checkout, send a packet into the WSL2 copy:

```powershell
.\windows-copilot\Invoke-KOSPrimeWsl.ps1 `
  -InputPath .\windows-copilot\sample-packet.json `
  -Distribution Ubuntu `
  -LinuxRepoPath "/home/your-ubuntu-user/kos-prime"
```

Run STAR-MESH inside WSL2 with:

```bash
cd ~/kos-prime
. .venv/bin/activate
python3 star_mesh_daemon.py --config star-mesh.json
```

Set `GEMINI_API_KEY` only in the WSL2 environment when live Gemini requests are intended. Without it, the adapter uses local mock mode.

## Boundaries

Windows provides the user-facing entrypoint. WSL2 provides Linux execution. STAR-MESH transports packets, and PrimeBus validates and routes them. Camera, microphone, and agent actions remain governed by `KOSPrime.M3tG1r.MultimodalGovernance`.