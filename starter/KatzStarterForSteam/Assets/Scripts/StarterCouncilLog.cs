using UnityEngine;
using UnityEngine.UI;

namespace KatzStarterForSteam;

public sealed class StarterCouncilLog : MonoBehaviour
{
    [SerializeField] private Text logText;

    private void Start()
    {
        if (logText != null)
            logText.text = string.Join("\n", StarterFakeData.CouncilEntries);
    }
}