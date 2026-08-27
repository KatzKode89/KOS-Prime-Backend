# K@tz-0$-St@rt3r-F0r-St3@m Final Specification

Version: `1.0.0`

`K@tz-0$-St@rt3r-F0r-St3@m` is a small Unity desktop/XR micro-cockpit for the Steam ecosystem. It is a conceptual teaser for Sovereign OS, not the KOS-Prime runtime.

## Included

- One `StarterCockpit.unity` scene.
- ShipCore panel with static or timer-driven presentation state.
- STAR-MESH mini-map with fake local nodes.
- SynthStack indicator with no real audio synthesis.
- Council log with prewritten local entries.
- Static or simple animated glyph overlay.
- Local timers and fake packets for visual flow only.

## Excluded

PrimeBus routing, tri-node runtime, STAR-MESH daemon, SynthStack audio engine, WSL2/Ubuntu services, Gemini, real glyph validation, persona logic, camera, microphone, network access, and external API keys.

## Distribution

- Target: Windows x86_64 Unity build, with SteamOS/Steam Deck considered only after a real Unity Linux build and hardware test.
- Store label: `Starter demo`, `Not full KOS-Prime`, `Uses fake data only`, `Concept cockpit preview`.
- The app should request no camera or microphone permissions and should not include network services.
- Use the Steam Deck `desktop-steam` profile unless XR support is deliberately added later.

## Licensing

The repository root [MIT License](../LICENSE) governs repository-owned material. [LICENSE-STARTER-NOTICE.md](../starter/KatzStarterForSteam/LICENSE-STARTER-NOTICE.md) documents the demo scope; it is not a modified MIT license and does not silently add non-commercial restrictions. Third-party Unity, Steamworks, platform, audio, art, and model assets retain their own terms.

## Build boundary

The backend repository contains source scripts and assembly guidance, not a complete Unity project. A Unity-capable Windows or CI host must create the scene, resolve serialized UI references, build `KatzStarterForSteam.exe`, and perform Steam depot validation.