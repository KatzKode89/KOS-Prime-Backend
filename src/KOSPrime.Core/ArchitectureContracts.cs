using KOSPrime.Bus;

namespace KOSPrime.Core.Architecture;

public enum ShipCoreModuleState
{
    Offline,
    Standby,
    Active,
    Degraded,
    Faulted
}

public sealed record ShipCoreModuleInput(PacketEnvelope Packet);

public sealed record ShipCoreModuleOutput(PacketEnvelope Packet);

public sealed record ShipCoreHealthReport(
    bool IsHealthy,
    string Status,
    IReadOnlyDictionary<string, double> Measurements);

public interface IShipCoreModule
{
    ModuleId ModuleName { get; }
    ShipCoreModuleState State { get; }
    ShipCoreModuleOutput Process(ShipCoreModuleInput input);
    ShipCoreHealthReport GetHealth();
}

public interface IPrimeBusEntrypoint
{
    RouteValidationResult Submit(PacketEnvelope packet);
}

public interface IPrimeBusTelemetrySink
{
    void Record(PacketEnvelope packet);
}