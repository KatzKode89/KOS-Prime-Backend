using KOSPrime.Bus;
using KOSPrime.Core;
using KOSPrime.Core.Architecture;
using Xunit;

namespace KOSPrime.Tests;

public sealed class ArchitectureContractsTests
{
    [Fact]
    public void ShipCoreModule_UsesPrimeBusPacketBoundary()
    {
        var module = new ContractModule();
        var packet = new PacketEnvelope
        {
            Source = ModuleId.CognitiveEngine,
            Destination = ModuleId.QuantumCrystals,
            Type = PacketType.Command,
            SequenceNumber = 1
        };

        var output = module.Process(new ShipCoreModuleInput(packet));

        Assert.Equal(ModuleId.QuantumCrystals, module.ModuleName);
        Assert.Equal(packet, output.Packet);
        Assert.Equal(ShipCoreModuleState.Active, module.State);
    }

    [Fact]
    public void EntrypointContract_SubmitsThroughPrimeBus()
    {
        var bus = new PrimeBus();
        bus.RegisterModule(ModuleId.CognitiveEngine);
        bus.RegisterModule(ModuleId.QuantumCrystals);
        IPrimeBusEntrypoint entrypoint = new BusEntrypoint(bus);

        var result = entrypoint.Submit(new PacketEnvelope
        {
            Source = ModuleId.CognitiveEngine,
            Destination = ModuleId.QuantumCrystals,
            SequenceNumber = 1
        });

        Assert.True(result.IsValid);
    }

    private sealed class ContractModule : IShipCoreModule
    {
        public ModuleId ModuleName => ModuleId.QuantumCrystals;
        public ShipCoreModuleState State { get; private set; } = ShipCoreModuleState.Standby;

        public ShipCoreModuleOutput Process(ShipCoreModuleInput input)
        {
            State = ShipCoreModuleState.Active;
            return new ShipCoreModuleOutput(input.Packet);
        }

        public ShipCoreHealthReport GetHealth() =>
            new(true, "STABLE", new Dictionary<string, double>());
    }

    private sealed class BusEntrypoint(IPrimeBus bus) : IPrimeBusEntrypoint
    {
        public RouteValidationResult Submit(PacketEnvelope packet) => bus.Publish(packet);
    }
}