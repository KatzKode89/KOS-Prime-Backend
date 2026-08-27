using UnityEngine;
using UnityEngine.UI;

namespace KatzStarterForSteam;

public sealed class StarterShipCoreController : MonoBehaviour
{
    [SerializeField] private Text statusText;
    [SerializeField] private Text integrityText;
    [SerializeField] private float updateInterval = 2f;

    private StarterShipStatus _status = new();
    private float _elapsed;

    private void Update()
    {
        _elapsed += Time.deltaTime;
        if (_elapsed < updateInterval) return;
        _elapsed = 0f;
        _status.integrity = Mathf.Max(0f, _status.integrity - 1f);
        _status.status = _status.integrity > 25f ? "NOMINAL" : "CAUTION";
        RefreshView();
    }

    private void Start() => RefreshView();

    private void RefreshView()
    {
        if (statusText != null) statusText.text = $"STATUS: {_status.status}";
        if (integrityText != null) integrityText.text = $"HULL: {_status.integrity:0}%";
    }
}