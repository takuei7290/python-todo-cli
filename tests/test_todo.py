from todo import add_task, load_tasks
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