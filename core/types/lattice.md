# Lattice Type

## Packet: `ShipCore_vOmega.Modules`

This packet describes the CrystalSeekers ship core internal module group. Its packet type is `lattice` because the group consumes crystal-lattice resonance and produces coordinated energy, navigation, and structural-integrity state.

### Envelope

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `packetType` | string | yes | Always `lattice`. |
| `ontologySegment` | string | yes | `ShipCore_vOmega.Modules`. |
| `moduleName` | string | yes | One of the five predefined Core Internal Modules. |
| `schemaVersion` | string | yes | Contract version, starting at `1.0`. |
| `sequence` | unsigned integer | yes | Monotonic module sequence number. |
| `timestamp` | UTC timestamp | yes | Time at which the sample or command was produced. |
| `correlationId` | string | no | Identifier for correlating input, output, and health events. |
| `state` | string | yes | State-machine state for the module sample. |
| `payload` | object | yes | Module-specific measurements, command values, or output vectors. |

### Module identifiers

The `moduleName` value must be one of:

1. `CrystalCoreResonanceChamber`
2. `HarmonicPhaseStabilizer`
3. `DimensionalNavigationMatrix`
4. `InertialDampeningGrid`
5. `ShieldHullIntegrityArray`

### Unity contract

The future Unity runtime should expose each module through the same shape of contract. The following is a conceptual interface boundary, not an implementation:

```csharp
public interface IShipCoreModule
{
	string ModuleName { get; }
	ShipCoreModuleState State { get; }
	ShipCoreModuleOutput Process(ShipCoreModuleInput input);
	ShipCoreHealthReport GetHealth();
}
```

Implementations must keep input and output transport on PrimeBus, use ontology-defined packet names, and leave persistence of telemetry to ReclusionMemory.