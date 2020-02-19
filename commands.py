import utils
import collections

class CommandQueue:
    def __init__(self):
        self._queue = collections.deque()

    def add(self, command):
        self._queue.append(command)

    def execute_commands(self):
        while self._queue:
            self._queue.popleft().execute()


class Command:
    def __init__(self,  func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def execute(self):
        self._func(*self._args, **self._kwargs)

class MoveCommand(Command): ...

class AttackCommand(Command): ...

