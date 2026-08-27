using KOSPrime.Bus;
using KOSPrime.Core;
using KOSPrime.Modules;
using Xunit;

namespace KOSPrime.Tests;

public sealed class PrimeBusRoutingTests
{
    [Fact]
    public void Publish_ValidRouteAndSequence_Succeeds()
    {
        var bus = new PrimeBus();
        bus.RegisterModule(ModuleId.CognitiveEngine);
        bus.RegisterModule(ModuleId.QuantumCrystals);

        var result = bus.Publish(CreatePacket(ModuleId.CognitiveEngine, ModuleId.QuantumCrystals, 1));

        Assert.True(result.IsValid);
    }

    [Fact]
    public void Publish_UnregisteredModule_FailsRouting()
    {
        var bus = new PrimeBus();
        bus.RegisterModule(ModuleId.QuantumCrystals);

        var result = bus.Publish(CreatePacket(ModuleId.CognitiveEngine, ModuleId.QuantumCrystals, 1));

        Assert.False(result.IsValid);
        Assert.Contains("not registered", result.ErrorMessage);
    }

    [Fact]
    public void Publish_UnknownOntologySegment_FailsRouting()
    {
        var bus = new PrimeBus();
        bus.RegisterModule(ModuleId.CognitiveEngine);
        bus.RegisterModule(ModuleId.QuantumCrystals);
        var packet = new PacketEnvelope
        {
            OntologySegment = "Unknown",
            Source = ModuleId.CognitiveEngine,
            Destination = ModuleId.QuantumCrystals,
            SequenceNumber = 1
        };

        var result = bus.Publish(packet);

        Assert.False(result.IsValid);
        Assert.Contains("ontology segment", result.ErrorMessage);
    }

    [Fact]
    public void Publish_DuplicateOrOutOfOrderSequence_RejectsPacket()
    {
        var bus = new PrimeBus();
        bus.RegisterModule(ModuleId.GenesisPulse);
        bus.RegisterModule(ModuleId.NaniteMesh);

        var firstResult = bus.Publish(CreatePacket(ModuleId.GenesisPulse, ModuleId.NaniteMesh, 5));
        var duplicateResult = bus.Publish(CreatePacket(ModuleId.GenesisPulse, ModuleId.NaniteMesh, 5));
        var olderResult = bus.Publish(CreatePacket(ModuleId.GenesisPulse, ModuleId.NaniteMesh, 4));

        Assert.True(firstResult.IsValid);
        Assert.False(duplicateResult.IsValid);
        Assert.False(olderResult.IsValid);
        Assert.Contains("Sequence rejection", duplicateResult.ErrorMessage);
    }

    [Fact]
    public void ShieldHullIntegrityArray_PublishesStableAndCriticalHealth()
    {
        var bus = new PrimeBus();
        bus.RegisterModule(ModuleId.QuantumCrystals);
        var packets = new List<PacketEnvelope>();
        using var subscription = bus.Subscribe(ModuleId.QuantumCrystals, packets.Add);
        var shieldModule = new ShieldHullIntegrityArray(bus);

        var stableResult = shieldModule.EvaluateIntegrity(85.0);
        var criticalResult = shieldModule.EvaluateIntegrity(10.0);

        Assert.True(stableResult.IsValid);
        Assert.True(criticalResult.IsValid);
        Assert.Collection(
            packets,
            packet => Assert.Equal("STABLE", packet.Payload["Status"]),
            packet => Assert.Equal("CRITICAL_FAULT", packet.Payload["Status"]));
    }

    [Fact]
    public void ShieldHullIntegrityArray_InvalidPercentage_IsRejected()
    {
        var bus = new PrimeBus();
        bus.RegisterModule(ModuleId.QuantumCrystals);
        var shieldModule = new ShieldHullIntegrityArray(bus);

        Assert.Throws<ArgumentOutOfRangeException>(() => shieldModule.EvaluateIntegrity(101));
    }

    private static PacketEnvelope CreatePacket(ModuleId source, ModuleId destination, long sequence) =>
        new()
        {
            Source = source,
            Destination = destination,
            Type = PacketType.Command,
            SequenceNumber = sequence
        };
}