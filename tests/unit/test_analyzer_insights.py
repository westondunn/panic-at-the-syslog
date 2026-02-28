from services.analyzer.app import AnalyzerService, FindingRealtime


def test_generate_insight_from_finding() -> None:
    """Test that analyzer generates schema-valid insights from findings."""
    service = AnalyzerService()
    finding = FindingRealtime(
        finding_id="find-001",
        correlation_id="corr-001",
        category="brute-force-suspected",
        confidence=0.82,
        details={"source_ip": "192.0.2.10", "attempts": 14},
    )

    insight = service.generate_insight(finding)

    assert insight.schema_version == "1.0"
    assert insight.finding_id == "find-001"
    assert insight.correlation_id == "corr-001"
    assert insight.summary is not None
    assert insight.recommendation is not None
    assert insight.rationale is not None
    assert insight.priority == "high"
    assert insight.confidence == 0.82


def test_insight_id_is_deterministic() -> None:
    """Test that insight IDs are deterministic and stable for the same finding."""
    service = AnalyzerService()
    finding = FindingRealtime(
        finding_id="find-stable",
        correlation_id="corr-001",
        category="dns-anomaly",
        confidence=0.5,
        details={},
    )

    insight_1 = service.generate_insight(finding)
    insight_2 = service.generate_insight(finding)

    assert insight_1.insight_id == insight_2.insight_id
    assert insight_1.insight_id.startswith("ins-")


def test_priority_derivation_from_confidence() -> None:
    """Test that priority is derived correctly from confidence thresholds."""
    service = AnalyzerService()

    test_cases = [
        (0.95, "critical"),
        (0.85, "high"),
        (0.65, "medium"),
        (0.30, "low"),
    ]

    for confidence, expected_priority in test_cases:
        finding = FindingRealtime(
            finding_id=f"find-conf-{confidence}",
            correlation_id="corr-test",
            category="wan-instability",
            confidence=confidence,
            details={},
        )
        insight = service.generate_insight(finding)
        assert insight.priority == expected_priority, (
            f"confidence {confidence} should map to priority {expected_priority}, "
            f"got {insight.priority}"
        )


def test_recommendation_derivation_from_category() -> None:
    """Test that recommendations are category-specific."""
    service = AnalyzerService()

    category_to_keyword = {
        "brute-force-suspected": "Block",
        "wan-instability": "WAN",
        "dns-anomaly": "DNS",
        "unknown-category": "Review evidence",
    }

    for category, expected_keyword in category_to_keyword.items():
        finding = FindingRealtime(
            finding_id=f"find-{category}",
            correlation_id="corr-test",
            category=category,
            confidence=0.7,
            details={},
        )
        insight = service.generate_insight(finding)
        assert expected_keyword in insight.recommendation, (
            f"Category {category} should produce recommendation with '{expected_keyword}', "
            f"got: {insight.recommendation}"
        )


def test_correlation_id_propagation() -> None:
    """Test that correlation_id from finding is preserved in insight."""
    service = AnalyzerService()
    original_correlation_id = "corr-trace-12345"

    finding = FindingRealtime(
        finding_id="find-trace",
        correlation_id=original_correlation_id,
        category="brute-force-suspected",
        confidence=0.75,
        details={},
    )

    insight = service.generate_insight(finding)

    assert insight.correlation_id == original_correlation_id


def test_insight_to_event_serialization() -> None:
    """Test that to_event() produces a valid event dict."""
    service = AnalyzerService()
    finding = FindingRealtime(
        finding_id="find-serialize",
        correlation_id="corr-001",
        category="dns-anomaly",
        confidence=0.6,
        details={"dns_query_rate": 1200},
    )

    insight = service.generate_insight(finding)
    event = insight.to_event()

    # Verify all required schema fields are present
    required_fields = [
        "schema_version",
        "insight_id",
        "finding_id",
        "correlation_id",
        "analyzed_at",
        "summary",
        "recommendation",
        "rationale",
        "priority",
        "confidence",
        "details",
    ]
    for field in required_fields:
        assert field in event, f"Event missing required field: {field}"

    # Verify schema version matches
    assert event["schema_version"] == "1.0"


def test_confidence_normalization() -> None:
    """Test that out-of-range confidence values are clamped to [0, 1]."""
    service = AnalyzerService()

    test_cases = [
        (-0.5, 0.0),
        (1.5, 1.0),
        (0.5, 0.5),
    ]

    for raw_confidence, expected_normalized in test_cases:
        finding = FindingRealtime(
            finding_id=f"find-clamp-{raw_confidence}",
            correlation_id="corr-test",
            category="brute-force-suspected",
            confidence=raw_confidence,
            details={},
        )
        insight = service.generate_insight(finding)
        assert insight.confidence == expected_normalized, (
            f"Confidence {raw_confidence} should normalize to {expected_normalized}, "
            f"got {insight.confidence}"
        )


def test_rationale_includes_attempt_count_when_available() -> None:
    """Test that rationale mentions attempt count if present in finding details."""
    service = AnalyzerService()

    finding_with_attempts = FindingRealtime(
        finding_id="find-attempts",
        correlation_id="corr-001",
        category="brute-force-suspected",
        confidence=0.8,
        details={"attempts": 42},
    )

    insight = service.generate_insight(finding_with_attempts)
    assert "42" in insight.rationale, "Rationale should mention the attempt count"
