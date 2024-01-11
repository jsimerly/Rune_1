from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Optional

class Clickable(ABC):
    @abstractmethod
    def on_click(self) -> Optional[Callable]:
        pass

class Draggable(ABC):
    @abstractmethod
    def on_drag_start(self):
        pass

    @abstractmethod
    def on_drag_update(self):
        pass

    @abstractmethod
    def on_drag_finish(self):
        pass

# Use to tell the game manager we want to keep current function
class ContinueAction:
    pass

