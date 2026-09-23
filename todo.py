import sys
import json
import os
from datetime import datetime

def load_tasks():
    if os.path.exists("tasks.json"):
            with open("tasks.json", "r", encoding="utf-8") as f:
                try:
                    tasks = json.load(f)
                    if not isinstance(tasks, list):
                        raise ValueError
                    
                except (json.JSONDecodeError, ValueError):
                    print("tasks.jsonの中身が壊れています")
                    sys.exit()
            return tasks

    else:
        tasks=[]
        return tasks

if len(sys.argv)<2:
    print("コマンドがありません。add / list / done / delete のいずれかを指定してください")
    sys.exit()


if sys.argv[1]=="add":

    tasks=load_tasks()

    if len(sys.argv)<3 or " ".join(sys.argv[2:]).strip()=="":
        print("内容を入力してください")

    else:
        new_task={
            "id": max((task["id"] for task in tasks) , default=0)+1 ,
            "content": " ".join(sys.argv[2:]) ,
            "done": False ,
            "created_at": str(datetime.now())
        }

        tasks.append(new_task)
        print("追加しました")
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False)

elif sys.argv[1]=="list":

    tasks=load_tasks()         

    if len(tasks)==0:
        print("タスクはありません")

    else:
        for task in tasks:
            if task["done"]==True:
                print(str(task["id"]) + ". " + task["content"] + " [完了]")
            else:
                print(str(task["id"]) + ". " + task["content"] + " [未完了]")

elif sys.argv[1]=="done":

    tasks=load_tasks()

    if len(sys.argv)<3:
            print("idを入力してください")

    else:
        found=False
        for task in tasks:
            if str(task["id"])==sys.argv[2]:
                task["done"]=True
                with open("tasks.json", "w", encoding="utf-8") as f:
                    json.dump(tasks, f, ensure_ascii=False)
                print("完了にしました")
                found=True

        if found==False:
            print("該当するタスクがありません")

elif sys.argv[1]=="delete":

    tasks=load_tasks() 

    new_tasks=[] 
    found=False

    if len(sys.argv)<3:
                print("idを入力してください")

    else:            
        for task in tasks:
            if str(task["id"])==sys.argv[2]:
                found=True

            else:
                new_tasks.append(task)

        if found==True:
            with open("tasks.json", "w", encoding="utf-8") as f:
                json.dump(new_tasks, f, ensure_ascii=False)
            print("削除しました")

        else:
            print("該当するタスクがありません")

else:
    print("そのコマンドは無効です")
    sys.exit()