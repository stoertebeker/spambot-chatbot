"""Tests für TimingManager."""
import json
import pytest
from src.timing_manager import TimingManager


def test_load_config_from_file(tmp_path):
    config = {"min_delay": 1.0, "max_delay": 5.0, "chars_per_second_min": 4.0}
    config_file = tmp_path / "timing.json"
    config_file.write_text(json.dumps(config), encoding="utf-8")

    tm = TimingManager(config_path=str(config_file))

    assert tm.get("min_delay") == 1.0
    assert tm.get("max_delay") == 5.0
    assert tm.get("chars_per_second_min") == 4.0


def test_default_config_when_file_missing(tmp_path):
    tm = TimingManager(config_path=str(tmp_path / "nonexistent.json"))

    assert tm.get("min_delay") == 2.0
    assert tm.get("max_delay") == 8.0


def test_default_config_written_to_disk(tmp_path):
    config_path = tmp_path / "timing.json"
    TimingManager(config_path=str(config_path))

    assert config_path.exists()
    data = json.loads(config_path.read_text())
    assert "min_delay" in data


def test_default_config_on_invalid_json(tmp_path):
    config_file = tmp_path / "bad.json"
    config_file.write_text("{ungültiges json", encoding="utf-8")

    tm = TimingManager(config_path=str(config_file))

    assert tm.get("min_delay") == 2.0


def test_get_returns_default_for_unknown_key(tmp_path):
    config_file = tmp_path / "timing.json"
    config_file.write_text(json.dumps({}), encoding="utf-8")

    tm = TimingManager(config_path=str(config_file))

    assert tm.get("nonexistent_key", 42) == 42


def test_get_all_returns_copy(tmp_path):
    config_file = tmp_path / "timing.json"
    config_file.write_text(json.dumps({"min_delay": 1.0}), encoding="utf-8")

    tm = TimingManager(config_path=str(config_file))
    all_config = tm.get_all()
    all_config["min_delay"] = 999

    assert tm.get("min_delay") == 1.0  # Original unverändert


def test_update_persists_to_disk(tmp_path):
    config_file = tmp_path / "timing.json"
    config_file.write_text(json.dumps({"min_delay": 1.0}), encoding="utf-8")

    tm = TimingManager(config_path=str(config_file))
    tm.update({"min_delay": 5.0, "new_key": "new_value"})

    data = json.loads(config_file.read_text())
    assert data["min_delay"] == 5.0
    assert data["new_key"] == "new_value"


def test_update_reflected_in_get(tmp_path):
    config_file = tmp_path / "timing.json"
    config_file.write_text(json.dumps({"min_delay": 1.0}), encoding="utf-8")

    tm = TimingManager(config_path=str(config_file))
    tm.update({"min_delay": 7.5})

    assert tm.get("min_delay") == 7.5
