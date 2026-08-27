using UnityEngine;

namespace KatzStarterForSteam;

public sealed class StarterGlyphOverlay : MonoBehaviour
{
    [SerializeField] private RectTransform glyphTransform;
    [SerializeField] private float pulseSpeed = 1.5f;
    [SerializeField] private float pulseScale = 0.08f;

    private Vector3 _baseScale;

    private void Start()
    {
        if (glyphTransform != null) _baseScale = glyphTransform.localScale;
    }

    private void Update()
    {
        if (glyphTransform == null) return;
        var pulse = 1f + Mathf.Sin(Time.time * pulseSpeed) * pulseScale;
        glyphTransform.localScale = _baseScale * pulse;
    }
}