using KOSPrime.Bus;
using KOSPrime.Core;

namespace KOSPrime.Modules;

public sealed class ShieldHullIntegrityArray
{
    public const double CriticalThreshold = 15.0;

    private readonly IPrimeBus _bus;
    private long _sequenceCounter;

    public ShieldHullIntegrityArray(IPrimeBus bus)
    {
        _bus = bus ?? throw new ArgumentNullException(nameof(bus));
        _bus.RegisterModule(ModuleId.ShieldHullIntegrityArray);
    }

    public RouteValidationResult EvaluateIntegrity(double currentIntegrityPercentage)
    {
        if (double.IsNaN(currentIntegrityPercentage) ||
            double.IsInfinity(currentIntegrityPercentage) ||
            currentIntegrityPercentage is < 0 or > 100)
        {
            throw new ArgumentOutOfRangeException(
                nameof(currentIntegrityPercentage),
                "Integrity percentage must be between 0 and 100.");
        }

        var packet = new PacketEnvelope
        {
            Source = ModuleId.ShieldHullIntegrityArray,
            Destination = ModuleId.QuantumCrystals,
            Type = PacketType.Health,
            SequenceNumber = Interlocked.Increment(ref _sequenceCounter),
            Payload = new Dictionary<string, object?>
            {
                ["IntegrityPercentage"] = currentIntegrityPercentage,
                ["Status"] = currentIntegrityPercentage <= CriticalThreshold
                    ? "CRITICAL_FAULT"
                    : "STABLE"
            }
        };

        return _bus.Publish(packet);
    }
}