# CrystalSeekers Steam Beta Distribution

## Product

- **Title:** CrystalSeekers: Echoes of Destiny
- **Package:** K@tz-0$-St@rt3r-F0r-St3@m
- **Version:** `0.1.0-beta`
- **Target:** Unity Windows x64 desktop demo
- **Scene:** `StarterCockpit.unity`

This is a small starter demo using fake local data. It is not the full KOS-Prime backend and does not require PrimeBus, WSL2, Gemini, STAR-MESH, camera, microphone, or real audio synthesis.

## Distribution workflow

1. Open the starter source in a Unity project.
2. Add `Assets/Scenes/StarterCockpit.unity` and `Assets/Prefabs/StarterPanels.prefab` according to [the scene guide](unity-starter-scene.md).
3. Import the starter C# scripts and resolve their UI references.
4. Build Windows x64 in Unity and smoke-test status, map, SynthStack preview, and council panels.
5. Run the package checker from the repository root:

```bash
python3 tools/package_steam_starter.py
```

6. Upload the Unity output to a Windows x64 Steam depot using publisher-managed Steamworks tooling.
7. Test the depot install on a clean Windows machine before publishing the Beta branch or demo app.

The source handoff ZIP is written to `dist/` and generated distribution artifacts are not committed.

## Store checklist

- App name, capsule art, screenshots, trailer, and description reviewed.
- Demo clearly labeled as a starter/concept experience.
- Hardware requirements and Windows x64 target verified.
- Unity runtime redistribution and third-party asset licenses reviewed.
- Steamworks SDK, App ID, depot, branch, and build account configured by the publisher.
- Crash reporting and privacy disclosures reviewed.
- No API keys, private model data, camera data, microphone data, or backend credentials in the build.
- Store copy does not claim full KOS-Prime functionality.

The actual Unity executable cannot be produced in this backend Codespace because Unity is not installed. A Unity-capable Windows or CI build agent is required for the final Steam depot artifact.