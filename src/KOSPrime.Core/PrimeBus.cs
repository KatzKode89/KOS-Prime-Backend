using System.Collections.Concurrent;
using KOSPrime.Core;

namespace KOSPrime.Bus;

public interface IPrimeBus
{
    void RegisterModule(ModuleId moduleId);
    RouteValidationResult Publish(PacketEnvelope packet);
    IDisposable Subscribe(ModuleId moduleId, Action<PacketEnvelope> handler);
}

public sealed class PrimeBus : IPrimeBus
{
    private readonly object _gate = new();
    private readonly HashSet<ModuleId> _registeredModules = new();
    private readonly Dictionary<ModuleId, long> _lastSequenceNumbers = new();
    private readonly ConcurrentDictionary<ModuleId, List<Action<PacketEnvelope>>> _subscriptions = new();

    public void RegisterModule(ModuleId moduleId)
    {
        lock (_gate)
        {
            _registeredModules.Add(moduleId);
            _lastSequenceNumbers.TryAdd(moduleId, 0);
        }
    }

    public RouteValidationResult Publish(PacketEnvelope packet)
    {
        ArgumentNullException.ThrowIfNull(packet);

        Action<PacketEnvelope>[] handlers;
        lock (_gate)
        {
            if (packet.OntologySegment != PacketEnvelope.ShipCoreOntologySegment)
            {
                return RouteValidationResult.Invalid(
                    $"Routing rejection: Unknown ontology segment '{packet.OntologySegment}'.");
            }

            if (!_registeredModules.Contains(packet.Source))
            {
                return RouteValidationResult.Invalid(
                    $"Routing rejection: Source module '{packet.Source}' is not registered.");
            }

            if (!_registeredModules.Contains(packet.Destination))
            {
                return RouteValidationResult.Invalid(
                    $"Routing rejection: Destination module '{packet.Destination}' is not registered.");
            }

            var lastSequence = _lastSequenceNumbers[packet.Source];
            if (packet.SequenceNumber <= lastSequence)
            {
                return RouteValidationResult.Invalid(
                    $"Sequence rejection: Packet sequence ({packet.SequenceNumber}) from " +
                    $"'{packet.Source}' must be greater than last recorded ({lastSequence}).");
            }

            _lastSequenceNumbers[packet.Source] = packet.SequenceNumber;
            handlers = _subscriptions.TryGetValue(packet.Destination, out var registeredHandlers)
                ? registeredHandlers.ToArray()
                : Array.Empty<Action<PacketEnvelope>>();
        }

        foreach (var handler in handlers)
        {
            try
            {
                handler(packet);
            }
            catch (Exception exception)
            {
                Console.Error.WriteLine($"Error delivering packet to {packet.Destination}: {exception.Message}");
            }
        }

        return RouteValidationResult.Valid();
    }

    public IDisposable Subscribe(ModuleId moduleId, Action<PacketEnvelope> handler)
    {
        ArgumentNullException.ThrowIfNull(handler);
        var handlers = _subscriptions.GetOrAdd(moduleId, _ => new List<Action<PacketEnvelope>>());
        lock (_gate)
        {
            handlers.Add(handler);
        }

        return new Subscription(() =>
        {
            lock (_gate)
            {
                handlers.Remove(handler);
            }
        });
    }

    private sealed class Subscription(Action unsubscribe) : IDisposable
    {
        private Action? _unsubscribe = unsubscribe;

        public void Dispose() => Interlocked.Exchange(ref _unsubscribe, null)?.Invoke();
    }
}