from dataclasses import dataclass, asdict, field
import json
from enum import Enum
import argparse
from datetime import datetime

class TaskStatus(Enum):
    NEW = "Новая"
    INPROGRESS = "Выполняется"
    INREVIEW = "Ревью"
    DONE = "Выполнено"
    CANCELLED = "Отменено"

@dataclass
class Task:
    name: str
    description: str
    status: TaskStatus
    createdat: datetime
    updatedat: datetime = field(default=datetime.now())

class TaskManager:
    def init(self):
        self.tasks = []

    def addtask(self, task: Task):
        self.tasks.append(task)

    def savetasks(self, filename):
        with open(filename, "w") as file:
            json.dump([asdict(task) for task in self.tasks], file, default=str)

    def loadtasks(self, filename):
        with open(filename, "r", encoding ="utf-8") as file:
            data = json.load(file)
            self.tasks = [Task(name=task['name'], description=task['description'], status=TaskStatus(task['status']), createdat=datetime.fromisoformat(task['created_at']), updatedat=datetime.fromisoformat(task['updatedat'])) for task in data]

    def viewtasks(self):
        for task in self.tasks:
            print(f"Название: {task.name}, Статус: {task.status.value}")
    
    def clean_tasks(self):
        self.tasks = []

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Название файла для сохранения/загрузки задач")
args = parser.parse_args()

manager = TaskManager()
manager.loadtasks(args.filename)
manager.viewtasks()

    # Пример добавления задачи

i = int(input("Хотите добавить задачу - 1, посмотреть список задач - 2, очистить список и завершить - 3: "))
while i!=3:
    if i == 1:
        name = input("Введите название задачи: ")
        description = input("Введите описание задачи: ")
        manager.addtask(Task(name, description, status=TaskStatus.NEW, createdat=datetime.now()))
    elif i == 2:
        manager.viewtasks()
    else:
        print("Действие незаконно!")
    i = int(input("Хотите добавить задачу - 1, посмотреть список задач - 2, очистить список и завершить - 3: "))

manager.clean_tasks()
manager.savetasks(args.filename)


    