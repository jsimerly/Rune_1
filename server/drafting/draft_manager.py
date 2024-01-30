from __future__ import annotations
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from .draft import Draft

class DraftManager:
    def __init__(self) -> None:
        self.active_drafts: Dict[str, Draft] = {} # draft_id : Draft
        
    def route_message(self, user, message):
        data = message['data']
        draft_id = data['draft_id']

        if draft_id in self.active_drafts:
            self.active_drafts[draft_id].handle_from_client(user, data)

    def add_draft(self, draft_obj: Draft):
        self.active_drafts[draft_obj.draft_id] = draft_obj

    
