using System;
using UnityEngine;

namespace KatzStarterForSteam;

[Serializable]
public sealed class StarterShipStatus
{
    public string status = "NOMINAL";
    [Range(0f, 100f)] public float integrity = 100f;
}

[Serializable]
public sealed class StarterMeshPoint
{
    public string label = "Echo Node";
    public Vector2 position;
}

public static class StarterFakeData
{
    public static StarterMeshPoint[] MeshPoints => new[]
    {
        new StarterMeshPoint { label = "Crystal Gate", position = new Vector2(-0.55f, 0.2f) },
        new StarterMeshPoint { label = "Echo Relay", position = new Vector2(0.25f, 0.45f) },
        new StarterMeshPoint { label = "Destiny Drift", position = new Vector2(0.5f, -0.3f) }
    };

    public static readonly string[] CouncilEntries =
    {
        "CognitiveEngine: course stable.",
        "ReclusionMemory: echo trace archived locally.",
        "GenesisOutput: starter signal ready."
    };
}