"""Tests für PersonalityManager."""
import json
from src.personality import PersonalityManager


def test_load_personality_from_file(tmp_path):
    config = {
        "name": "TestBot",
        "system_prompt": "Du bist ein Test.",
        "age": 25,
        "occupation": "Tester",
        "background": "Testumgebung",
        "interests": ["pytest", "coverage"]
    }
    config_file = tmp_path / "personality.json"
    config_file.write_text(json.dumps(config), encoding="utf-8")

    pm = PersonalityManager(config_path=str(config_file))

    assert pm.get_name() == "TestBot"
    assert pm.get_system_prompt() == "Du bist ein Test."


def test_default_personality_when_file_missing(tmp_path):
    pm = PersonalityManager(config_path=str(tmp_path / "nonexistent.json"))

    assert pm.get_name() == "Anna"
    assert "freundliche" in pm.get_system_prompt()


def test_default_personality_on_invalid_json(tmp_path):
    config_file = tmp_path / "bad.json"
    config_file.write_text("{ungültiges json", encoding="utf-8")

    pm = PersonalityManager(config_path=str(config_file))

    assert pm.get_name() == "Anna"


def test_get_full_context_contains_all_fields(tmp_path):
    config = {
        "name": "Lena",
        "age": 30,
        "occupation": "Ärztin",
        "background": "Hannover",
        "interests": ["Lesen", "Kochen"],
        "system_prompt": "Test"
    }
    config_file = tmp_path / "personality.json"
    config_file.write_text(json.dumps(config), encoding="utf-8")

    pm = PersonalityManager(config_path=str(config_file))
    context = pm.get_full_context()

    assert "Lena" in context
    assert "30" in context
    assert "Ärztin" in context
    assert "Hannover" in context
    assert "Lesen" in context
    assert "Kochen" in context


def test_get_name_fallback_when_key_missing(tmp_path):
    config_file = tmp_path / "personality.json"
    config_file.write_text(json.dumps({"system_prompt": "Nur Prompt"}), encoding="utf-8")

    pm = PersonalityManager(config_path=str(config_file))

    assert pm.get_name() == "Bot"


def test_get_system_prompt_fallback_when_key_missing(tmp_path):
    config_file = tmp_path / "personality.json"
    config_file.write_text(json.dumps({"name": "Nur Name"}), encoding="utf-8")

    pm = PersonalityManager(config_path=str(config_file))

    assert pm.get_system_prompt() == "Du bist ein hilfreicher Chatbot."
