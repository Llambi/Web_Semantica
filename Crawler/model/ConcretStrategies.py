from abc import ABC
from typing import Deque


class QueueStrategy(ABC):
    def extend(self, data, queue: Deque):
        pass


class WidthStrategy(QueueStrategy):
    def extend(self, data, queue: Deque):
        queue.extend(data)


class DeepStrategy(QueueStrategy):
    def extend(self, data, queue: Deque):
        queue.extendleft(data)
