# K@tz-0$-St3@m-D3ck

Version: `1.0.0`

This is the Steam generation, compiler, designer, and distribution framework for KOS-Prime app and game projects. It supports Steam Windows, SteamOS/Linux, Steam Deck, Steam Link, Big Picture, and controller-first operation through explicit build profiles.

## Designer and world generator

Create a deterministic app or game design with a custom world seed:

```bash
python3 tools/steam_stack.py new game "CrystalSeekers: Echoes of Destiny" \
  --seed 4242 \
  --output /tmp/crystalseekers-beta
python3 tools/steam_stack.py validate /tmp/crystalseekers-beta
```

The generated `steam-build.json` and `world.json` are build inputs. The world generator is deterministic and local; it does not call Gemini, access private training data, or create network services.

## Compiler framework

The compiler adapter validates the manifest and invokes an installed Unity Editor in batch mode:

```bash
python3 tools/steam_stack.py compile /path/to/unity-project \
  --unity-editor /path/to/Unity \
  --output ./build/windows-x64
```

This repository cannot run that command without a Unity project and Unity Editor. A production pipeline should produce separate Windows x64, Linux x64, and Steam Deck test artifacts.

## Platform profiles

- **Steam Windows**: Windows x64 desktop build with keyboard, mouse, and Steam Input.
- **SteamOS/Linux**: native Linux build where supported, otherwise a publisher-tested Proton build.
- **Steam Deck**: controller-first UI, readable 1280x800 layout, suspend/resume handling, safe-area margins, and conservative performance settings.
- **Steam Link**: low-latency input, scalable UI, resilient reconnect handling, and no assumption that the host display is local.
- **Big Picture**: focus navigation, gamepad-only operation, large status typography, and no hover-only controls.
- **VR/MR/XR**: optional OpenXR adapter from `docs/xr-frameworks.md`; desktop Steam mode remains available.

## Controller optimizer

[steam-controller-actions.json](../config/steam-controller-actions.json) defines the shared action set. Use Steam Input rather than vendor-specific gameplay calls, retain keyboard/mouse fallback, and never map an execute-tier action without the Sovereign OS confirmation flow.

## Distributor

Package a validated design input for handoff:

```bash
python3 tools/steam_stack.py package /tmp/crystalseekers-beta \
  --output ./dist/crystalseekers-beta-design.zip
```

The ZIP includes a SHA-256 digest in command output and the Steam Deck profile. Publisher-managed Steamworks configuration remains outside this repository: App ID, depots, branches, release keys, store metadata, and upload credentials must be supplied by the publisher through secure tooling.

## Licensing

The repository root [MIT License](../LICENSE) remains authoritative for repository-owned source and documentation. Third-party Unity, Steamworks, Proton, controller, audio, art, and model assets retain their own licenses. Never put Steamworks credentials, signing keys, API keys, or private model content in generated manifests or packages.