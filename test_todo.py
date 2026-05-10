# Tests for todo.py
# Run with: python3 -m pytest test_todo.py -v
#
# Two pytest tools used here:
#   tmp_path     — gives each test its own temporary folder so tests don't touch your real tasks.json
#   monkeypatch  — lets us fake input() so we can test functions that ask the user to type something
#   capsys       — lets us capture printed output and check it in tests

import json
import pytest
import todo


# --- Helper fixture ---
# This runs before each test that asks for it.
# It points todo.TASKS_FILE at a temporary file so real tasks.json is never touched.

@pytest.fixture
def temp_tasks_file(tmp_path, monkeypatch):
    temp_file = tmp_path / "tasks.json"
    monkeypatch.setattr(todo, "TASKS_FILE", str(temp_file))
    return temp_file


# --- Tests for load_tasks() ---

def test_load_tasks_file_does_not_exist(temp_tasks_file):
    # If no file exists yet, should return an empty list
    result = todo.load_tasks()
    assert result == []

def test_load_tasks_returns_saved_tasks(temp_tasks_file):
    # Write some tasks to the temp file and check that load_tasks reads them back
    tasks = [{"name": "Buy milk", "done": False}]
    temp_tasks_file.write_text(json.dumps(tasks))
    result = todo.load_tasks()
    assert result == tasks

def test_load_tasks_corrupted_file_returns_empty(temp_tasks_file, capsys):
    # If the file contains invalid JSON, should return [] and print a warning
    temp_tasks_file.write_text("this is not valid json!!!")
    result = todo.load_tasks()
    assert result == []
    printed = capsys.readouterr().out
    assert "corrupted" in printed


# --- Tests for save_tasks() ---

def test_save_tasks_writes_to_file(temp_tasks_file):
    # After saving, the file should contain the tasks we passed in
    tasks = [{"name": "Walk the dog", "done": False}]
    todo.save_tasks(tasks)
    content = json.loads(temp_tasks_file.read_text())
    assert content == tasks

def test_save_tasks_overwrites_existing_file(temp_tasks_file):
    # Saving a new list should replace whatever was in the file before
    todo.save_tasks([{"name": "Old task", "done": False}])
    todo.save_tasks([{"name": "New task", "done": True}])
    content = json.loads(temp_tasks_file.read_text())
    assert len(content) == 1
    assert content[0]["name"] == "New task"


# --- Tests for list_tasks() ---

def test_list_tasks_empty(capsys):
    # An empty list should print a helpful message
    todo.list_tasks([])
    printed = capsys.readouterr().out
    assert "No tasks yet" in printed

def test_list_tasks_shows_task_names(capsys):
    # Task names should appear in the output
    tasks = [{"name": "Buy milk", "done": False}, {"name": "Walk dog", "done": True}]
    todo.list_tasks(tasks)
    printed = capsys.readouterr().out
    assert "Buy milk" in printed
    assert "Walk dog" in printed

def test_list_tasks_shows_done_status(capsys):
    # Done tasks should show [x], not-done tasks should show [ ]
    tasks = [{"name": "Done task", "done": True}, {"name": "Pending task", "done": False}]
    todo.list_tasks(tasks)
    printed = capsys.readouterr().out
    assert "[x]" in printed
    assert "[ ]" in printed


# --- Tests for add_task() ---

def test_add_task_adds_to_list(temp_tasks_file, monkeypatch):
    # Simulate the user typing "Buy milk" when prompted
    monkeypatch.setattr("builtins.input", lambda _: "Buy milk")
    tasks = []
    todo.add_task(tasks)
    assert len(tasks) == 1
    assert tasks[0]["name"] == "Buy milk"
    assert tasks[0]["done"] == False

def test_add_task_empty_name_does_not_add(temp_tasks_file, monkeypatch, capsys):
    # Simulate the user pressing Enter with no text
    monkeypatch.setattr("builtins.input", lambda _: "")
    tasks = []
    todo.add_task(tasks)
    assert len(tasks) == 0
    printed = capsys.readouterr().out
    assert "empty" in printed

def test_add_task_saves_to_file(temp_tasks_file, monkeypatch):
    # After adding a task it should be saved in the file
    monkeypatch.setattr("builtins.input", lambda _: "Read a book")
    tasks = []
    todo.add_task(tasks)
    content = json.loads(temp_tasks_file.read_text())
    assert content[0]["name"] == "Read a book"


# --- Tests for complete_task() ---

def test_complete_task_marks_done(temp_tasks_file, monkeypatch):
    # Simulate the user picking task number 1
    monkeypatch.setattr("builtins.input", lambda _: "1")
    tasks = [{"name": "Buy milk", "done": False}]
    todo.complete_task(tasks)
    assert tasks[0]["done"] == True

def test_complete_task_on_empty_list(temp_tasks_file, monkeypatch, capsys):
    # With no tasks, should print a message and do nothing
    todo.complete_task([])
    printed = capsys.readouterr().out
    assert "No tasks yet" in printed


# --- Tests for delete_task() ---

def test_delete_task_removes_correct_task(temp_tasks_file, monkeypatch):
    # Simulate the user picking task number 1
    monkeypatch.setattr("builtins.input", lambda _: "1")
    tasks = [{"name": "Buy milk", "done": False}, {"name": "Walk dog", "done": False}]
    todo.delete_task(tasks)
    assert len(tasks) == 1
    assert tasks[0]["name"] == "Walk dog"

def test_delete_task_on_empty_list(temp_tasks_file, monkeypatch, capsys):
    # With no tasks, should print a message and do nothing
    todo.delete_task([])
    printed = capsys.readouterr().out
    assert "No tasks yet" in printed


# --- Tests for get_task_number() ---

def test_get_task_number_valid_input(monkeypatch):
    # User types "1" — should return index 0 (zero-based)
    monkeypatch.setattr("builtins.input", lambda _: "1")
    tasks = [{"name": "Task A", "done": False}]
    result = todo.get_task_number(tasks, "Pick: ")
    assert result == 0

def test_get_task_number_invalid_then_valid(monkeypatch):
    # User first types "abc", then "1" — should keep asking until valid
    responses = iter(["abc", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    tasks = [{"name": "Task A", "done": False}]
    result = todo.get_task_number(tasks, "Pick: ")
    assert result == 0

def test_get_task_number_out_of_range_then_valid(monkeypatch):
    # User first types "99", then "1" — should reject 99 and accept 1
    responses = iter(["99", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    tasks = [{"name": "Task A", "done": False}]
    result = todo.get_task_number(tasks, "Pick: ")
    assert result == 0
