from typing import Callable, Dict, List, Any

class EventManager:
    def __init__(self) -> None:
        self.events: Dict[Any, List[Callable]] = {}
        self.selected_obj = None

    def register_event(self, obj, fn: Callable):
        if obj  in self.events:
            self.events[obj].append(fn)
        else:
            self.events[obj] = fn

    def unregister(self, obj):
        del self.events[obj]

    def run_events_for(self, obj):
        fn = self.events[obj]
        fn()
    
class OnClickEventManager(EventManager):
    def __init__(self) -> None:
        super().__init__()
        self.clickable_obj: List = []

    def register_event(self, obj, fn: Callable):
        self.clickable_obj.append(obj)
        return super().register_event(obj, fn)