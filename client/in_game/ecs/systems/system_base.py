from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, List, Type

if TYPE_CHECKING:
    from components.component_base import Component
    from entity import Entity

class System(ABC):
    required_components = []

    def __init__(self) -> None:
        self._required_components: List[Type[Component]] = self.required_components
        self.entities: List[Entity] = []

    def add_entity(self, entity: Entity):
        if self.validate_entity_components(entity):
            self.entities.append(entity)
        else:
            raise ValueError(f"Entity must have these components: {self._required_components}")

    def validate_entity_components(self, entity: Entity):
        for required_component in self._required_components:
            if not entity.has_component(required_component):
                return False
        return True