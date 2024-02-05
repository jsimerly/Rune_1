from __future__ import annotations

from in_game.ecs.entity import Entity
from in_game.ecs.components.screen_position_component import ScreenPositionComponent
from in_game.ecs.components.ui_components import RectUIComponent, ClickableComponent

import pygame as pg
from abc import abstractmethod
from in_game.ecs.systems.render_systems import RenderSystem

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from entity import Entity

class UISystem(RenderSystem):
    required_components = [RectUIComponent, ScreenPositionComponent]

    def draw(self, display: pg.Surface):
        for entity in self.entities:
            self.draw_entity(display, entity)

    def draw_entity(self, display: pg.Surface, entity: Entity):
        rect_ui_component: RectUIComponent = entity.get_component(RectUIComponent)
        screen_position_component: ScreenPositionComponent = entity.get_component(ScreenPositionComponent)

        if rect_ui_component.image:
            display.blit(rect_ui_component.image, screen_position_component.position)
        
        if rect_ui_component.outline:
            rect = pg.Rect(screen_position_component.position, rect_ui_component.size)
            pg.draw.rect(display, rect_ui_component.outline_color, rect, rect_ui_component.outline_thickness)

    def find_clicked_obj(self, pixel: tuple(int,int)):
        for entity in self.entities:
            if entity.has_component(ClickableComponent):
                rect_component: RectUIComponent = entity.get_component(RectUIComponent)
                screen_position_component: ScreenPositionComponent = entity.get_component(ScreenPositionComponent)

                pos = screen_position_component.position
                size = rect_component.size
                rect = pg.Rect(pos, size)
                if rect.collidepoint(pixel):
                    return entity
                
    
