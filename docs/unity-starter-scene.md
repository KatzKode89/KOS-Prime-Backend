# CrystalSeekers Starter Scene

This guide assembles the local-only `K@tz-0$-St@rt3r-F0r-St3@m` demo in Unity.

## Scene

Create `Assets/Scenes/StarterCockpit.unity` with a Canvas containing four panels:

1. **ShipCore Status**: two UI Text controls for status and hull integrity. Add `StarterShipCoreController` and assign both fields.
2. **STAR-MESH Mini-Map**: a RectTransform map root and a small Image point prefab. Add `StarterStarMeshController` and assign the root and point prefab.
3. **SynthStack Indicator**: static UI text such as `SYNTHSTACK: PREVIEW ONLY`. Do not attach an audio source or claim synthesis is active.
4. **Council Log**: a multiline UI Text control. Add `StarterCouncilLog` and assign the log field.

Save the scene as `StarterCockpit.unity` and optionally create `Assets/Prefabs/StarterPanels.prefab` from the Canvas panel hierarchy.

## Build target

Use Unity's Windows x86_64 target for a local Steam demo build. The scripts use UnityEngine UI only and have no backend, network, WSL2, Gemini, camera, microphone, or Steamworks dependency.

The map points and council entries are fake local data. The timer-driven hull value is a presentation effect, not a real health check.