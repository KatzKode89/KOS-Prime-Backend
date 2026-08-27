# KOS-Prime VR, MR, and XR Framework Support

Version: `1.0.0`

This is the integration contract for Unity applications and games consuming the Sovereign OS cockpit. It favors OpenXR and Unity abstractions for portability, then adds platform adapters only where a device-specific capability is required.

## Support matrix

| Framework or platform | Target | Use in KOS-Prime | Adoption rule |
| --- | --- | --- | --- |
| Unity XR Plug-in Management | Unity app/game | Select and configure XR loaders per build target. | Required foundation for Unity XR builds. |
| OpenXR | Cross-vendor VR/MR/XR | Headset, controller, hand, and extension capability baseline. | Preferred runtime standard. Test required extensions per device. |
| XR Interaction Toolkit | Unity interaction layer | Ray/direct interaction, locomotion, interactors, and UI input. | Preferred shared interaction abstraction. |
| AR Foundation | Mobile AR/MR | Plane, anchor, raycast, camera, and environment tracking. | Use for AR-capable app builds; keep tracking permissions explicit. |
| Meta XR / Meta OpenXR | Quest and Horizon devices | Quest passthrough, hand tracking, controller features, and platform services. | Optional adapter behind OpenXR/XR interfaces. |
| Windows Mixed Reality / Windows XR | Windows HMD and MR devices | Windows-specific spatial input and device capabilities. | Optional legacy/platform adapter; do not make it the core contract. |
| SteamVR / OpenVR | SteamVR PC headsets | Steam desktop distribution and older runtime compatibility. | Optional compatibility path; prefer OpenXR for new work. |
| Unity Input System | App/game input | Map controllers, hands, keyboard, gamepad, and accessibility input. | Required for device-agnostic input actions. |
| Unity UI / world-space Canvas | Desktop/XR cockpit | Render ShipCore, STAR-MESH, glyph, council, and SynthStack panels. | Keep presentation separate from PrimeBus. |
| Unity Audio / DSPGraph | Sound layer | Consume SynthStack metadata through an audio adapter. | Optional; starter demo uses preview-only UI. |

“Support” means a documented adapter boundary, not that every SDK or device is installed in this repository. Version-specific package compatibility must be verified in the Unity project and on target hardware.

## App developer contract

Applications should prioritize accessibility, setup, privacy, and short interaction flows:

- Use OpenXR/XR Interaction Toolkit where available and provide a non-XR desktop fallback.
- Request camera, microphone, hand, and spatial-mapping permissions only when a feature is enabled.
- Expose independent text, voice, sound, and visual-attention controls.
- Bind panels to validated read-only packets by default.
- Keep all state-changing controls in the `observe -> suggest -> draft -> confirm -> execute` governance flow.
- Provide keyboard, controller, gaze, and screen-reader alternatives for critical controls.

## Game developer contract

Games may use XR for cockpit presence, world-space UI, locomotion, interaction, audio, and haptics:

- Use the Input System action map instead of vendor-specific input calls in gameplay code.
- Keep locomotion and comfort settings configurable, including snap turning, vignette, seated mode, and recentering.
- Drive game state from deterministic local systems or PrimeBus contracts, never from glyphs or camera attention alone.
- Treat SynthStack sound/voice as an adapter so gameplay remains testable without audio hardware.
- Provide a desktop spectator or non-XR mode for Steam builds where practical.

## Sovereign OS bindings

Unity adapters consume `KOSPrime.SovereignOS.UnityCockpit`, `KOSPrime.GlyphSystem`, `SynthStack_vOmega.Sound`, and `SynthStack_vOmega.Voice`. PrimeBus remains the routing authority; STAR-MESH remains transport. Camera attention is metadata only and never authorizes an action.

## Build profiles

Recommended profiles are:

- `desktop-steam`: Windows x64, no headset required, keyboard/gamepad fallback.
- `openxr-pc`: Windows x64 with OpenXR and XR Interaction Toolkit.
- `quest-openxr`: Android/Quest with OpenXR and optional Meta adapter.
- `mobile-ar`: Android/iOS with AR Foundation and explicit camera permission.

Each profile should have a separate Unity quality setting, input action validation pass, permission review, and hardware smoke test. This backend repository supplies contracts and cannot run those Unity validation passes without a Unity project and target device.