from abc import ABC

class Component(ABC):
    def __init__(self) -> None:
        ...

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"


