from todo import add_task, load_tasks, done_task, delete_task, list_tasks
import os
import pytest

@pytest.fixture
def clean_test_file():
    if os.path.exists("test_tasks.json"):
        os.remove("test_tasks.json")

def test_add_task(clean_test_file):
    add_task("テストタスク", "test_tasks.json")
    tasks = load_tasks("test_tasks.json")
    assert len(tasks) == 1
    assert tasks[0]["content"] == "テストタスク"

def test_add_task_empty(clean_test_file):
    add_task("", "test_tasks.json")
    tasks = load_tasks("test_tasks.json")
    assert len(tasks) == 0

def test_add_task_id_increment(clean_test_file):
    add_task("1個目", "test_tasks.json")
    add_task("2個目", "test_tasks.json")
    tasks = load_tasks("test_tasks.json")
    assert tasks[1]["id"]==2

def test_done_task(clean_test_file):
    add_task("テストタスク", "test_tasks.json")
    done_task("1", "test_tasks.json")
    tasks = load_tasks("test_tasks.json")
    assert tasks[0]["done"]==True

def test_done_task_not_found(clean_test_file):
    add_task("テストタスク", "test_tasks.json")
    done_task("2", "test_tasks.json")
    tasks = load_tasks("test_tasks.json")
    assert tasks[0]["done"]==False

def test_delete_task(clean_test_file):
    add_task("テストタスク", "test_tasks.json")
    delete_task("1", "test_tasks.json")
    tasks = load_tasks("test_tasks.json")
    assert len(tasks) == 0

def test_delete_task_not_found(clean_test_file):
    add_task("テストタスク", "test_tasks.json")
    delete_task("2", "test_tasks.json")
    tasks = load_tasks("test_tasks.json")
    assert len(tasks) == 1

def test_delete_task_multiple(clean_test_file):
    add_task("1個目", "test_tasks.json")
    add_task("2個目", "test_tasks.json")
    delete_task("1", "test_tasks.json")
    tasks = load_tasks("test_tasks.json")
    assert len(tasks) == 1
    assert tasks[0]["content"] == "2個目"

def test_list_tasks_empty(clean_test_file, capsys):
    list_tasks("test_tasks.json")
    output = capsys.readouterr().out
    assert "タスクはありません" in output

def test_list_tasks_with_tasks(clean_test_file, capsys):
    add_task("テストタスク", "test_tasks.json")
    list_tasks("test_tasks.json")
    output = capsys.readouterr().out
    assert "テストタスク" in output

def test_list_tasks_done(clean_test_file, capsys):
    add_task("テストタスク", "test_tasks.json")
    done_task("1", "test_tasks.json")
    list_tasks("test_tasks.json")
    output = capsys.readouterr().out
    assert "[完了]" in output