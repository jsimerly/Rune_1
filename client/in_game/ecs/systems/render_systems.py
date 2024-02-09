from __future__ import annotations

from in_game.ecs.entity import Entity
from in_game.event_bus import EventBus
from .system_base import System
from in_game.ecs.components.sprite_component import TileSpriteComponent, SpriteComponent
from in_game.ecs.components.visual_edge_component import VisualHexEdgeComponent, SelectedHexEdgeComponent
from in_game.ecs.components.screen_position_component import ScreenPositionComponent
from typing import Optional
import pygame as pg
from abc import abstractmethod

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from map.tile import GameTile
    from entity import Entity
    from action_state import ActionState

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

    def __init__(self, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        event_bus.subscribe('spawn_to_tile', self.entity_to_tile)

    def draw_entity(self, display:pg.Surface, entity: Entity):
        sprite_component: Optional[SpriteComponent] = entity.get_component(SpriteComponent)
        position_component: ScreenPositionComponent = entity.get_component(ScreenPositionComponent)
        if sprite_component.is_visible and position_component.position:
            pos = self.get_top_left_position(sprite_component.image, position_component.position)
            display.blit(sprite_component.image, pos)

    def entity_to_tile(self, tile: GameTile, entity: Entity):
        center_pixel = tile.center_pixel
        sprite_comp: SpriteComponent = entity.get_component(SpriteComponent)
        position_comp: ScreenPositionComponent = entity.get_component(ScreenPositionComponent)

        pos = (
            center_pixel[0],
            center_pixel[1] - 20 #this is assuming radius of tile is 36
        )

        sprite_comp.is_visible = True
        position_comp.position = pos



class DrawHexEdgeSystem(RenderSystem):
    required_components = [VisualHexEdgeComponent, ScreenPositionComponent]

    def __init__(self, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self.event_bus.subscribe('idle_enter', self.reset_all_edges)

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

    def update_to_single_entity(self, entity: Entity):
        self.entities = [entity]

    def reset_all_edges(self):
        for entity in self.entities:
            visual_component: Optional[VisualHexEdgeComponent] = entity.get_component(VisualHexEdgeComponent)
            if visual_component:
                visual_component.color = visual_component.default_color
                visual_component.thickness = visual_component.default_thickness
                visual_component.transparent = visual_component.default_transparency

class DrawSelectedHexSystem(RenderSystem):
    required_components = [SelectedHexEdgeComponent, ScreenPositionComponent]

    def __init__(self, event_bus: EventBus, action_state: ActionState) -> None:
        super().__init__(event_bus)
        self.action_state: ActionState = action_state
        self.event_bus.subscribe('tile_selected', self.add_entity)
        

    def add_entity(self, tile: GameTile):
        self.entities = [tile]

    def draw(self, display: pg.Surface):
        if self.action_state.is_idle:
            for entity in self.entities:
                self.draw_entity(display, entity)

    def draw_entity(self, display:pg.Surface, tile: GameTile):
        visual_component: Optional[SelectedHexEdgeComponent] = tile.get_component(SelectedHexEdgeComponent)
        if visual_component:
            pg.draw.polygon(display, visual_component.color, visual_component.verticies, visual_component.thickness)

    



    


