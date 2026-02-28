from libs.common.config import load_settings


def test_settings_default_openai_plugin_disabled() -> None:
    settings = load_settings()
    assert settings.openai_plugin_enabled is False