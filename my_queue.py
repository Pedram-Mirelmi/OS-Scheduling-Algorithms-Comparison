from modulefinder import LOAD_CONST
from queue import Queue, PriorityQueue
from threading import Lock
from tkinter.messagebox import NO

# Pedram - Mirelmi - 610398176

class ScopedLock:
    def __init__(self, lock: Lock) -> None:
        self.lock = lock
        self.lock.acquire()

    def __del__(self):
        self.lock.release()

class MyQueue:
    def __init__(self) -> None:
        
        self.queue = Queue()
        # self.lock = Lock()

    def enqueue(self, item):
        # lock = ScopedLock(self.lock)
        self.queue.put(item)

    
    def dequeue(self):
        # lock = ScopedLock(self.lock)
        if self.queue.empty():
            raise Exception("tried to dequeue from empty queue")
        else:
            item = self.queue.get()

        return item
    
    def isEmpty(self):
        # lock = ScopedLock(self.lock)
        is_empty = self.queue.empty()
        return is_empty
    
class MyPriorityQueue:
    def __init__(self) -> None:
        self.queue = PriorityQueue()
        # self.lock = Lock()

    def enqueue(self, item):
        # lock = ScopedLock(self.lock)
        self.queue.put(item)

    
    def dequeue(self):
        # lock = ScopedLock(self.lock)
        if self.queue.empty():
            raise Exception("tried to dequeue from empty queue")
        else:
            item = self.queue.get()

        return item
    
    def isEmpty(self):
        # lock = ScopedLock(self.lock)
        is_empty = self.queue.empty()
        return is_empty

    def next(self):
        # lock = ScopedLock(self.lock)
        if self.queue.empty():
            return None
        return self.queue.queue[0]

    
