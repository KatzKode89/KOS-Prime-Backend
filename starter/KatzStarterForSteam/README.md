# K@tz-0$-St@rt3r-F0r-St3@m

## CrystalSeekers: Echoes of Destiny Starter Demo

This is a deliberately small Unity desktop demo concept for Steam. It presents the feel of Sovereign OS through one local cockpit scene and fake data only.

### Scope

- Single scene: `Assets/Scenes/StarterCockpit.unity`
- ShipCore status panel with timer-driven demo state
- STAR-MESH mini-map with fake points
- SynthStack indicator with no audio synthesis
- Council log with prewritten entries
- Local C# logic only

This starter demo is **not the full KOS-Prime system**. It has no WSL2 integration, Ubuntu services, PrimeBus routing engine, STAR-MESH daemon, Gemini calls, camera input, microphone input, or real synthesis. It must not be marketed as those systems.

## Unity layout

```text
KatzStarterForSteam/
  Assets/
    Scenes/StarterCockpit.unity
    Prefabs/StarterPanels.prefab
    Scripts/
      StarterFakeData.cs
      StarterShipCoreController.cs
      StarterStarMeshController.cs
      StarterCouncilLog.cs
  LICENSE-STARTER-NOTICE.md
```

Import the scripts into a Unity project, create the scene and UI bindings described in [docs/unity-starter-scene.md](../../../docs/unity-starter-scene.md), and target Windows x64 for a Steam demo build. Steamworks integration, packaging, and store configuration are intentionally outside this starter source package.

The starter targets the `desktop-steam` profile. XR support is optional; developers may add OpenXR and XR Interaction Toolkit later, but this Beta remains playable without a headset.

The repository-wide [MIT License](../../../LICENSE) remains authoritative for repository content. The starter notice documents its scope and does not add a non-commercial restriction under the MIT name.