from abc import ABC, abstractmethod

class AbstactGameState(ABC):
    @abstractmethod
    def on_enter(self):
        ...

    @abstractmethod
    def on_exit(self):
        ...

    @abstractmethod
    def handle_server_message(self):
        ...