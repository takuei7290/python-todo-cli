import pytest

from todo import add_task, build_parser, delete_task, done_task, list_tasks, load_tasks


def test_add_task(tmp_path):
    filename = tmp_path / "test_tasks.json"
    add_task("テストタスク", filename)
    tasks = load_tasks(filename)
    assert len(tasks) == 1
    assert tasks[0]["content"] == "テストタスク"


def test_add_task_empty(tmp_path):
    filename = tmp_path / "test_tasks.json"
    add_task("", filename)
    tasks = load_tasks(filename)
    assert len(tasks) == 0


def test_add_task_id_increment(tmp_path):
    filename = tmp_path / "test_tasks.json"
    add_task("1個目", filename)
    add_task("2個目", filename)
    tasks = load_tasks(filename)
    assert tasks[1]["id"] == 2


def test_done_task(tmp_path):
    filename = tmp_path / "test_tasks.json"
    add_task("テストタスク", filename)
    done_task("1", filename)
    tasks = load_tasks(filename)
    assert tasks[0]["done"] is True


def test_done_task_not_found(tmp_path):
    filename = tmp_path / "test_tasks.json"
    add_task("テストタスク", filename)
    done_task("2", filename)
    tasks = load_tasks(filename)
    assert tasks[0]["done"] is False


def test_delete_task(tmp_path):
    filename = tmp_path / "test_tasks.json"
    add_task("テストタスク", filename)
    delete_task("1", filename)
    tasks = load_tasks(filename)
    assert len(tasks) == 0


def test_delete_task_not_found(tmp_path):
    filename = tmp_path / "test_tasks.json"
    add_task("テストタスク", filename)
    delete_task("2", filename)
    tasks = load_tasks(filename)
    assert len(tasks) == 1


def test_delete_task_multiple(tmp_path):
    filename = tmp_path / "test_tasks.json"
    add_task("1個目", filename)
    add_task("2個目", filename)
    delete_task("1", filename)
    tasks = load_tasks(filename)
    assert len(tasks) == 1
    assert tasks[0]["content"] == "2個目"


def test_list_tasks_empty(tmp_path, capsys):
    filename = tmp_path / "test_tasks.json"
    list_tasks(filename)
    output = capsys.readouterr().out
    assert "タスクはありません" in output


def test_list_tasks_with_tasks(tmp_path, capsys):
    filename = tmp_path / "test_tasks.json"
    add_task("テストタスク", filename)
    list_tasks(filename)
    output = capsys.readouterr().out
    assert "テストタスク" in output


def test_list_tasks_done(tmp_path, capsys):
    filename = tmp_path / "test_tasks.json"
    add_task("テストタスク", filename)
    done_task("1", filename)
    list_tasks(filename)
    output = capsys.readouterr().out
    assert "[完了]" in output


def test_load_tasks_broken_json(tmp_path):
    filename = tmp_path / "test_tasks.json"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("これはJSONではない")
    with pytest.raises(SystemExit):
        load_tasks(filename)


def test_load_tasks_not_list(tmp_path):
    filename = tmp_path / "test_tasks.json"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("{}")
    with pytest.raises(SystemExit):
        load_tasks(filename)


def test_parser_no_command():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_parser_unknown_command():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["unknown"])


def test_parser_done():
    parser = build_parser()
    args = parser.parse_args(["done", "1"])
    assert args.command == "done"
    assert args.task_id == "1"


def test_parser_done_without_id():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["done"])


def test_parser_add():
    parser = build_parser()
    args = parser.parse_args(["add", "テスト", "をする"])
    assert args.command == "add"
    assert args.content == ["テスト", "をする"]


def test_parser_add_without_content():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["add"])
