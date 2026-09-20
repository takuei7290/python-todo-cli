import sys
import json
import os
from datetime import datetime

if sys.argv[1]=="add":

    if os.path.exists("tasks.json"):
        with open("tasks.json", "r", encoding="utf-8") as f:
            tasks = json.load(f)

    else:
        tasks=[]

    new_task={
        "id": len(tasks) + 1 ,
        "content": sys.argv[2] ,
        "done": False ,
        "created_at": str(datetime.now())
    }

    tasks.append(new_task)
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False)

elif sys.argv[1]=="list":

    if os.path.exists("tasks.json"):
            with open("tasks.json", "r", encoding="utf-8") as f:
                tasks = json.load(f)

    else:
            tasks=[]           


    if len(tasks)==0:
        print("タスクはありません")

    else:
        for task in tasks:
            if task["done"]==True:
                print(str(task["id"]) + ". " + task["content"] + " [完了]")
            else:
                print(str(task["id"]) + ". " + task["content"] + " [未完了]")