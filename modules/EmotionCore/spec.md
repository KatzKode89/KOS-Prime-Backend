# EmotionCore

## Bounded State Processor

EmotionCore converts observable input features into a bounded, inspectable state vector for response policy. It does not represent subjective experience or hidden feelings.

### Inputs

- User text and intent embeddings.
- Packet type and ontology segment.
- Session features such as turn count, topic volatility, and error rate.
- Telemetry from PrimeBus and GenesisOutput.

### State

`EmotionState` is a versioned lattice payload with four normalized fields:

```json
{
  "mood": 0.0,
  "energy": 0.0,
  "focus": 0.0,
  "tension": 0.0
}
```

Each field is hard-clamped to `[-1.0, 1.0]`. Values are policy signals, not claims about an internal mental state.

### Inference and smoothing

A small MLP or lightweight transformer head may produce the raw vector. Temporal smoothing applies a configured alpha:

```text
E_t = alpha * e_t + (1 - alpha) * E_(t-1)
```

The implementation must constrain `alpha` to `[0.0, 1.0]`, apply hard bounds after smoothing, and apply decay toward the configured neutral baseline when input is absent. Model version, alpha, bounds, and feature provenance must be logged with the state packet.

### Output

EmotionCore emits `KOSPrime.Emotion.State` as a `lattice` packet to CognitiveEngine and PersonalityPolicy through PrimeBus. ReclusionMemory may persist the packet subject to retention policy.