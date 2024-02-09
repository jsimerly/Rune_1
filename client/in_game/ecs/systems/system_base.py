from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, List, Type

if TYPE_CHECKING:
    from components.component_base import Component
    from entity import Entity
    from event_bus import EventBus

class System(ABC):
    required_components = []

    def __init__(self, event_bus: EventBus) -> None:
        self._required_components: List[Type[Component]] = self.required_components
        self.event_bus: EventBus = event_bus
        self.entities: List[Entity] = []

    def add_entity(self, entity: Entity):
        if self.validate_entity_components(entity):
            self.entities.append(entity)
        else:
            required_component_names = [comp.__name__ for comp in self._required_components]
            print(f"{self.__class__.__name__} must have these components: {', '.join(required_component_names)}")
            raise ValueError(f"{self.__class__.__name__} must have these components: {', '.join(required_component_names)}")

    def validate_entity_components(self, entity: Entity):
        for required_component in self._required_components:
            if not entity.has_component(required_component):
                return False
        return True