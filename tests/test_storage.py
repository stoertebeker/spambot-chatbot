"""Tests für BotStorage."""
import json
import pytest
from src.storage import BotStorage


def test_save_and_load_state(tmp_path):
    storage = BotStorage(filepath=str(tmp_path / "state.json"))
    active = {1, 2, 3}
    examples = {1: ["Hallo", "Hi"], 2: ["Hey"]}

    storage.save_state(active, examples)
    loaded_active, loaded_examples = storage.load_state()

    assert loaded_active == active
    assert loaded_examples == examples


def test_load_state_returns_empty_when_no_file(tmp_path):
    storage = BotStorage(filepath=str(tmp_path / "nonexistent.json"))

    active, examples = storage.load_state()

    assert active == set()
    assert examples == {}


def test_save_state_with_conversation_history(tmp_path):
    storage = BotStorage(filepath=str(tmp_path / "state.json"))
    history = {1: [{"role": "user", "content": "Hallo"}]}

    storage.save_state({1}, {}, conversation_history=history)

    data = json.loads((tmp_path / "state.json").read_text())
    assert "conversation_history" in data
    assert data["conversation_history"]["1"][0]["content"] == "Hallo"


def test_save_state_without_history_omits_key(tmp_path):
    storage = BotStorage(filepath=str(tmp_path / "state.json"))

    storage.save_state({1}, {})

    data = json.loads((tmp_path / "state.json").read_text())
    assert "conversation_history" not in data


def test_clear_state_removes_file(tmp_path):
    state_file = tmp_path / "state.json"
    storage = BotStorage(filepath=str(state_file))
    storage.save_state({1}, {})

    storage.clear_state()

    assert not state_file.exists()


def test_clear_state_noop_when_no_file(tmp_path):
    storage = BotStorage(filepath=str(tmp_path / "nonexistent.json"))
    storage.clear_state()  # Darf keinen Fehler werfen


def test_save_and_load_session(tmp_path):
    storage = BotStorage(filepath=str(tmp_path / "state.json"))

    storage.save_session("mein-session-string")
    result = storage.load_session()

    assert result == "mein-session-string"


def test_load_session_returns_empty_when_no_file(tmp_path):
    storage = BotStorage(filepath=str(tmp_path / "state.json"))

    result = storage.load_session()

    assert result == ""


def test_state_version_is_written(tmp_path):
    storage = BotStorage(filepath=str(tmp_path / "state.json"))
    storage.save_state({42}, {})

    data = json.loads((tmp_path / "state.json").read_text())
    assert data.get("version") == "2.0"


def test_load_state_with_corrupted_file(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text("{kaputt", encoding="utf-8")
    storage = BotStorage(filepath=str(state_file))

    active, examples = storage.load_state()

    assert active == set()
    assert examples == {}
