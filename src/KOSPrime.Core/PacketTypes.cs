using System.Collections.Generic;

namespace KOSPrime.Core;

public enum PacketType
{
    Command,
    State,
    Telemetry,
    Health
}

public enum ModuleId
{
    CognitiveEngine,
    ReclusionMemory,
    GenesisOutput,
    ChaosField,
    ReclusionCore,
    GenesisPulse,
    NaniteMesh,
    QuantumCrystals,
    CrystalCoreResonanceChamber,
    HarmonicPhaseStabilizer,
    DimensionalNavigationMatrix,
    InertialDampeningGrid,
    ShieldHullIntegrityArray
}

public sealed class PacketEnvelope
{
    public const string ShipCoreOntologySegment = "ShipCore_vOmega.Modules";

    public string PacketId { get; init; } = Guid.NewGuid().ToString("N");
    public string OntologySegment { get; init; } = ShipCoreOntologySegment;
    public ModuleId Source { get; init; }
    public ModuleId Destination { get; init; }
    public PacketType Type { get; init; }
    public long SequenceNumber { get; init; }
    public DateTime Timestamp { get; init; } = DateTime.UtcNow;
    public IReadOnlyDictionary<string, object?> Payload { get; init; } =
        new Dictionary<string, object?>();
}

public sealed class RouteValidationResult
{
    private RouteValidationResult(bool isValid, string errorMessage)
    {
        IsValid = isValid;
        ErrorMessage = errorMessage;
    }

    public bool IsValid { get; }
    public string ErrorMessage { get; }

    public static RouteValidationResult Valid() => new(true, string.Empty);

    public static RouteValidationResult Invalid(string message) => new(false, message);
}