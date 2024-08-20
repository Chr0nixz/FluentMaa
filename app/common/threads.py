import time

from PySide6.QtCore import QThread, Signal, QObject, QMutex
from qfluentwidgets import StateToolTip


class Task(QObject):
    def __init__(self, target, trigger=None, signal: Signal = None):
        super().__init__()
        self.target = target
        self.trigger = trigger
        self.signal = signal

    def run(self):
        result = self.target()
        if self.signal:
            if result:
                self.signal.emit(result)
            else:
                self.signal.emit()


class TaskGroup(QObject):
    def __init__(self, tasks=None, trigger=None, signal=None):
        super().__init__()
        if not tasks:
            tasks = []
        self.tasks = tasks
        self.trigger = trigger
        self.signal = signal

    def addTask(self, task):
        self.tasks.append(task)

    def run(self):
        for task in self.tasks:
            task.run()
        if self.signal:
            self.signal.emit()


class Threads:
    class ThreadsManager(QThread):
        def __init__(self, pool):
            super().__init__()
            self.pool = pool

        def run(self):
            while True:
                if self.pool:
                    for i, t in self.pool.items():
                        print(t)
                time.sleep(1)

    def __init__(self):
        self.pool = {}
        self.manager = Threads.ThreadsManager(self.pool)
        self.manager.start()

    def addTaskRun(self, task):
        tid = len(self.pool)
        thread = QThread()
        task.moveToThread(thread)
        thread.started.connect(task.run)
        thread.finished.connect(lambda: self.pool.pop(tid))
        self.pool[tid] = thread
        thread.start()
        print(self.pool)

    def addTask(self, task: Task) -> int:
        tid = len(self.pool)
        thread = QThread()
        task.moveToThread(thread)
        if task.trigger:
            task.trigger.connect(thread.run)
        thread.started.connect(task.run)
        thread.finished.connect(lambda: self.pool.pop(tid))
        self.pool[tid] = thread
        print(self.pool)
        return tid

    def addTaskGroupRun(self, taskGroup: TaskGroup):
        tid = len(self.pool)
        thread = QThread()
        taskGroup.moveToThread(thread)
        thread.run = taskGroup.run
        #thread.started.connect(taskGroup.run)
        thread.finished.connect(lambda: self.pool.pop(tid))
        self.pool[tid] = thread
        print(self.pool)
        thread.start()

    def addThreadRun(self, thread: QThread):
        tid = len(self.pool)
        thread.finished.connect(lambda: self.pool.pop(tid))
        self.pool[tid] = thread
        print(self.pool)
        thread.start()

    def process(self, target):
        tid = len(self.pool)
        thread = QThread(target=target)
        thread.start()
        self.pool[tid] = thread

    def clear(self):
        for i, t in self.pool.items():
            t.terminate()
        self.pool.clear()


threads = Threads()
mutex = QMutex()
