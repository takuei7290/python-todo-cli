import argparse
import json
import os
import sys
from datetime import datetime


def load_tasks(filename="tasks.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                tasks = json.load(f)
                if not isinstance(tasks, list):
                    raise TypeError

            except (json.JSONDecodeError, TypeError):
                print("tasks.jsonの中身が壊れています")
                sys.exit()
        return tasks

    else:
        tasks = []
        return tasks


def save_tasks(tasks, filename="tasks.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False)


def list_tasks(filename="tasks.json"):
    tasks = load_tasks(filename)

    if len(tasks) == 0:
        print("タスクはありません")

    else:
        for task in tasks:
            if task["done"]:
                print(str(task["id"]) + ". " + task["content"] + " [完了]")
            else:
                print(str(task["id"]) + ". " + task["content"] + " [未完了]")


def add_task(content, filename="tasks.json"):
    tasks = load_tasks(filename)

    if content.strip() == "":
        print("内容を入力してください")

    else:
        new_task = {
            "id": max((task["id"] for task in tasks), default=0) + 1,
            "content": content,
            "done": False,
            "created_at": str(datetime.now()),
        }

        tasks.append(new_task)
        print("追加しました")
        save_tasks(tasks, filename)


def done_task(task_id, filename="tasks.json"):
    tasks = load_tasks(filename)

    found = False
    for task in tasks:
        if str(task["id"]) == task_id:
            task["done"] = True
            save_tasks(tasks, filename)
            print("完了にしました")
            found = True

    if not found:
        print("該当するタスクがありません")


def delete_task(task_id, filename="tasks.json"):
    tasks = load_tasks(filename)

    new_tasks = []
    found = False
    for task in tasks:
        if str(task["id"]) == task_id:
            found = True

        else:
            new_tasks.append(task)

    if found:
        save_tasks(new_tasks, filename)
        print("削除しました")

    else:
        print("該当するタスクがありません")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ToDoを管理するCLIツール")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="タスクを追加する")
    add_parser.add_argument("content", nargs="+", help="タスクの内容")

    subparsers.add_parser("list", help="タスクの一覧を表示する")

    done_parser = subparsers.add_parser("done", help="タスクを完了にする")
    done_parser.add_argument("task_id", help="完了にするタスクのid")

    delete_parser = subparsers.add_parser("delete", help="タスクを削除する")
    delete_parser.add_argument("task_id", help="削除するタスクのid")

    args = parser.parse_args()

    if args.command == "add":
        add_task(" ".join(args.content))

    elif args.command == "list":
        list_tasks()

    elif args.command == "done":
        done_task(args.task_id)

    elif args.command == "delete":
        delete_task(args.task_id)
