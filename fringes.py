class Stack:
    def __init__(self):
        self.stack = []
    def empty(self):
        return len(self.stack) == 0
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        if self.empty():
            raise Exception('Stack is empty')
        return self.stack.pop()
    def peek(self):
        if self.empty():
            raise Exception('Stack is empty')
        return self.stack[-1]

class Queue:
    def __init__(self):
        self.items = []
    def empty(self):
        return len(self.items) == 0
    def enqueue(self, item):
        self.items.append(item)
    def dequeue(self):
        if self.empty():
            raise Exception('Queue is empty')
        return self.items.pop(0)
    def peek(self):
        if self.empty():
            raise Exception('Queue is empty')
        return self.items[0]
    def size(self):
        return len(self.items)
    
class PriorityQueue:
    def __init__(self):
        self.items = []
    def empty(self):
        return len(self.items) == 0
    
    def put(self, priority, item):
        node = (priority, item)
        for i, (p, _) in enumerate(self.items):
            if priority < p:
                self.items.insert(i, node)
                break
        else:
            self.items.append(node)

    def put(self, item):
            self.items.append(item)
    def get(self):
        if self.empty():
            raise Exception('PriorityQueue is empty')
        return self.items.pop(0)
    def size(self):
        return len(self.items)

