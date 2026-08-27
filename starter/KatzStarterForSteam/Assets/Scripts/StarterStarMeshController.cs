using UnityEngine;
using UnityEngine.UI;

namespace KatzStarterForSteam;

public sealed class StarterStarMeshController : MonoBehaviour
{
    [SerializeField] private RectTransform mapRoot;
    [SerializeField] private Image pointPrefab;

    private void Start()
    {
        if (mapRoot == null || pointPrefab == null) return;
        foreach (var point in StarterFakeData.MeshPoints)
        {
            var view = Instantiate(pointPrefab, mapRoot);
            view.rectTransform.anchorMin = (point.position + Vector2.one) * 0.5f;
            view.rectTransform.anchorMax = view.rectTransform.anchorMin;
            view.rectTransform.anchoredPosition = Vector2.zero;
        }
    }
}