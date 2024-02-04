from __future__ import annotations
from typing import TYPE_CHECKING, Type, List, Dict, Optional
from abc import ABC

if TYPE_CHECKING:
    from components.component_base import Component
    from systems.system_base import System

class Entity(ABC):
    required_components = []
    def __init__(self, components: List[Component] = None) -> None:
        self.components: Dict[Type[Component], Component] =  {}
        for component in components:
            self.components[type(component)] = component

        all_required_components = self.combine_required_components()
        for required_component in all_required_components:
            if required_component not in self.components:
                raise ValueError(f"{required_component} is required for this Entity.")
            
    @classmethod
    def combine_required_components(cls) -> List[Type[Component]]:
        components = cls.required_components
        for base in cls.__bases__:
            if issubclass(base, Entity) and hasattr(base, 'required_components'):
                components.extend(base.required_components)
        return list(set(components))
        
    def add_or_update_component(self, component: Component):
        self.components[type(component)] = component

    def get_component(self, component_type: Type[Component]) -> Optional[Component]:
        if component_type in self.components:
            return self.components[component_type]
        return None
            
    def has_component(self, component_type: Type[Component]):
        return component_type in self.components



    

            


