from abc import ABC
from typing import Callable

class EventBus:
    def __init__(self) -> None:
        self.listeners: dict[str, list[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def publish(self, event_type: str, data):
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                callback(data)


