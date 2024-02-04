from __future__ import annotations
from .system_base import System
from in_game.ecs.components.sprite_component import TileSpriteComponent, SpriteComponent
from in_game.ecs.components.visual_edge_component import VisualHexEdgeComponent
from in_game.ecs.components.screen_position_component import ScreenPositionComponent
from in_game.map.tile import GameTile
from typing import Optional
import pygame as pg
from abc import abstractmethod

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from entity import Entity

class RenderSystem(System):
    def draw(self, display: pg.Surface):
        for entity in self.entities:
            self.draw_entity(display, entity)
    
    @abstractmethod
    def draw_entity(self, display: pg.Surface, entity: Entity):
        ...
        
    def get_top_left_position(self, image: pg.Surface, start_pos: Tuple[int,int]):
        image_size = image.get_size()
        
        x_pos = start_pos[0] - image_size[0]//2
        y_pos = start_pos[1] - image_size[1]//2
        return (x_pos, y_pos)
    
class DrawTileSystem(RenderSystem):
    required_components = [TileSpriteComponent, ScreenPositionComponent]
    pg.font.init()
    font = pg.font.SysFont(None, 26)

    def draw_entity(self, display:pg.Surface, entity: Entity):
        sprite_component: TileSpriteComponent = entity.get_component(TileSpriteComponent)
        position_component: ScreenPositionComponent = entity.get_component(ScreenPositionComponent)

        if sprite_component.is_visible:
            pg.draw.polygon(display, sprite_component.bg_color, sprite_component.verticies)
            pos = self.get_top_left_position(sprite_component.image, position_component.position)
            display.blit(sprite_component.image, pos)

        ''' Uncomment to turn coordinates on'''
        # if isinstance(entity, GameTile):
        #     if True:
        #         point = entity.center_pixel
        #         text = f'{entity.q}, {entity.r}'
        #         text_surface = self.font.render(text, True, (0, 0, 0))
        #         text_pos = (point[0] - text_surface.get_width() // 2, point[1] - text_surface.get_height() // 2)

        #         display.blit(text_surface, text_pos)  

class DrawSpriteSystem(RenderSystem):
    required_components = [SpriteComponent, ScreenPositionComponent]

    def draw_entity(self, display:pg.Surface, entity: Entity):
        sprite_component: Optional[SpriteComponent] = entity.get_component(SpriteComponent)
        position_component: ScreenPositionComponent = entity.get_component(ScreenPositionComponent)
        if  sprite_component.is_visible:
            pos = self.get_top_left_position(sprite_component.image, position_component.position)
            display.blit(sprite_component.image, pos)

class DrawHexEdgeSystem(RenderSystem):
    required_components = [VisualHexEdgeComponent, ScreenPositionComponent]

    def draw(self, display: pg.Surface):
        trans_surface = pg.Surface(display.get_size(), pg.SRCALPHA)
        trans_surface.fill((0, 0, 0, 0))
        for entity in self.entities:
            self.draw_entity(display, entity, trans_surface)

        display.blit(trans_surface, (0,0))


    def draw_entity(self, display:pg.Surface, entity: Entity, trans_surface):
        visual_component: Optional[VisualHexEdgeComponent] = entity.get_component(VisualHexEdgeComponent)
        if visual_component:
            if visual_component.transparent:
                pg.draw.polygon(trans_surface, visual_component.color, visual_component.verticies, visual_component.thickness)
            else:
                pg.draw.polygon(display, visual_component.color, visual_component.verticies, visual_component.thickness)

    





    


