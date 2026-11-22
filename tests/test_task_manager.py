import json

import pytest

import task_manager as tm


@pytest.fixture(autouse=True)
def tmp_tasks_file(tmp_path, monkeypatch):
    path = tmp_path / "tasks.json"
    monkeypatch.setattr(tm, "TASKS_FILE", str(path))
    return path


def test_load_missing_file_returns_empty():
    assert tm.load_tasks() == []


def test_add_persists(tmp_tasks_file):
    tasks = []
    tm.add_task(tasks, "buy milk")
    assert json.loads(tmp_tasks_file.read_text()) == [{"description": "buy milk", "completed": False}]
    assert tm.load_tasks() == tasks


def test_mark_completed_and_delete():
    tasks = []
    tm.add_task(tasks, "a")
    tm.add_task(tasks, "b")
    tm.mark_completed(tasks, 1)
    assert tasks[0]["completed"] is True
    tm.delete_task(tasks, 2)
    assert tm.load_tasks() == [{"description": "a", "completed": True}]


@pytest.mark.parametrize("idx", [0, 3, -1])
def test_invalid_index_does_not_change(idx, capsys):
    tasks = [{"description": "a", "completed": False}]
    tm.mark_completed(tasks, idx)
    tm.delete_task(tasks, idx)
    assert tasks == [{"description": "a", "completed": False}]
    assert "Invalid task index" in capsys.readouterr().out


def test_corrupted_file_does_not_crash(tmp_tasks_file):
    tmp_tasks_file.write_text("{not json")
    assert tm.load_tasks() == []


def test_main_non_numeric_index_does_not_crash(monkeypatch, capsys):
    inputs = iter(["3", "abc", "4", "x", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    tm.main()
    assert "valid number" in capsys.readouterr().out


def test_main_rejects_empty_description(monkeypatch):
    inputs = iter(["1", "   ", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    tm.main()
    assert tm.load_tasks() == []
