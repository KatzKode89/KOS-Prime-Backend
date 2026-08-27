using System.Text.Json;
using KOSPrime.Bus;
using KOSPrime.Core;
using KOSPrime.Modules;

var integrity = 85.0;
if (args.Length == 2 && args[0] == "--health" && double.TryParse(args[1], out var requestedIntegrity))
{
    integrity = requestedIntegrity;
}
else if (args.Length != 0)
{
    Console.Error.WriteLine("Usage: KOSPrime.Runner.exe [--health <0-100>]");
    return 2;
}

var bus = new PrimeBus();
bus.RegisterModule(ModuleId.QuantumCrystals);
PacketEnvelope? emittedPacket = null;
using var subscription = bus.Subscribe(ModuleId.QuantumCrystals, packet => emittedPacket = packet);
var shield = new ShieldHullIntegrityArray(bus);
var route = shield.EvaluateIntegrity(integrity);

var result = new
{
    route.IsValid,
    route.ErrorMessage,
    Packet = emittedPacket == null
        ? null
        : new
        {
            emittedPacket.PacketId,
            emittedPacket.OntologySegment,
            emittedPacket.Source,
            emittedPacket.Destination,
            emittedPacket.Type,
            emittedPacket.SequenceNumber,
            emittedPacket.Payload
        }
};

Console.WriteLine(JsonSerializer.Serialize(result, new JsonSerializerOptions { WriteIndented = true }));
return route.IsValid ? 0 : 1;