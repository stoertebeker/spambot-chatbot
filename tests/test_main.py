from src.main import validate_environment


def test_validate_environment_fails_when_required_vars_missing(monkeypatch):
    monkeypatch.delenv("TELEGRAM_API_ID", raising=False)
    monkeypatch.delenv("TELEGRAM_API_HASH", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("LITELLM_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    error = validate_environment()

    assert error is not None
    assert "TELEGRAM_API_ID" in error
    assert "TELEGRAM_API_HASH" in error
    assert "LLM_API_KEY" in error


def test_validate_environment_passes_when_required_vars_exist(monkeypatch):
    monkeypatch.setenv("TELEGRAM_API_ID", "123456")
    monkeypatch.setenv("TELEGRAM_API_HASH", "abc123")
    monkeypatch.setenv("OPENAI_API_KEY", "dummy-key")

    error = validate_environment()

    assert error is None
