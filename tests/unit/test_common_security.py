from libs.common.security import redact_payload


def test_redact_payload_masks_sensitive_keys() -> None:
    payload = {
        "token": "top-secret",
        "message": "safe",
    }

    redacted = redact_payload(payload)

    assert redacted["token"] == "***REDACTED***"
    assert redacted["message"] == "safe"