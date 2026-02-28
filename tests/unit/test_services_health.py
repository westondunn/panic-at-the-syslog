from services.analyzer.app import AnalyzerService
from services.api.app import ApiService
from services.detector.app import DetectorService
from services.normalizer.app import NormalizerService


def test_health_endpoints_return_ok() -> None:
    services = [AnalyzerService(), ApiService(), DetectorService(), NormalizerService()]
    for service in services:
        health = service.health()
        assert health["status"] == "ok"
        assert "service" in health