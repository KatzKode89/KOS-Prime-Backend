# QuantumCrystal State Machine

## Ship core module lifecycle

Each Core Internal Module reports one of these states in its `lattice` packet:

- `Offline`: not initialized or unavailable.
- `Standby`: initialized and waiting for a command.
- `Active`: processing valid inputs and producing outputs.
- `Degraded`: operating with a threshold breach or incomplete input.
- `Faulted`: unable to produce a trusted output.

### Allowed transitions

```text
Offline -> Standby -> Active
Active -> Standby
Active -> Degraded
Degraded -> Active
Standby -> Offline
Active -> Faulted
Degraded -> Faulted
Faulted -> Offline
```

Transitions are emitted as `module.state` and `module.health` packets. CognitiveEngine owns control decisions, while ReclusionMemory records the transition and its correlated telemetry. A module must not transition directly from `Faulted` to `Active` without reinitialization through `Offline` and `Standby`.

The Shield & Hull Integrity Array enters `Degraded` when resonance-dampening efficacy falls below its configured threshold and enters `Faulted` when structural-integrity measurements are unavailable or invalid.