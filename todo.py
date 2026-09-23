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

def save_tasks(tasks):
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False)

def list_tasks():
    tasks=load_tasks()         

    if len(tasks)==0:
        print("タスクはありません")

    else:
        for task in tasks:
            if task["done"]==True:
                print(str(task["id"]) + ". " + task["content"] + " [完了]")
            else:
                print(str(task["id"]) + ". " + task["content"] + " [未完了]")

def add_task(content):
    tasks=load_tasks()
    
    if content.strip()=="":
            print("内容を入力してください")
    
    else:
        new_task={
            "id": max((task["id"] for task in tasks) , default=0)+1 ,
            "content": content ,
            "done": False ,
            "created_at": str(datetime.now())
        }
    
        tasks.append(new_task)
        print("追加しました")
        save_tasks(tasks)

def done_task(task_id):
    tasks=load_tasks()

    found=False
    for task in tasks:
        if str(task["id"])==task_id:
            task["done"]=True
            save_tasks(tasks)
            print("完了にしました")
            found=True

    if found==False:
        print("該当するタスクがありません")     

def delete_task(task_id):
    tasks=load_tasks() 

    new_tasks=[] 
    found=False
    for task in tasks:
        if str(task["id"])==task_id:
            found=True

        else:
            new_tasks.append(task)

    if found==True:
        save_tasks(new_tasks)
        print("削除しました")

    else:
        print("該当するタスクがありません")
   

if len(sys.argv)<2:
    print("コマンドがありません。add / list / done / delete のいずれかを指定してください")
    sys.exit()

if sys.argv[1]=="add":
    add_task(" ".join(sys.argv[2:]))

elif sys.argv[1]=="list":
    list_tasks()

elif sys.argv[1]=="done":
    if len(sys.argv)<3:
        print("idを入力してください")

    else:
        done_task(sys.argv[2])

elif sys.argv[1]=="delete":
    if len(sys.argv)<3:
        print("idを入力してください")

    else:            
        delete_task(sys.argv[2])

else:
    print("そのコマンドは無効です")
    sys.exit()