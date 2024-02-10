from __future__ import annotations

from in_game.ecs.entity import Entity
from in_game.event_bus import EventBus
from .system_base import System
from in_game.ecs.components.sprite_component import TileSpriteComponent, SpriteComponent
from in_game.ecs.components.visual_edge_component import VisualHexEdgeComponent, SelectedHexEdgeComponent
from in_game.ecs.components.fog_of_war import FogOfWarComponent
from in_game.ecs.components.screen_position_component import ScreenPositionComponent
from in_game.ecs.components.visual_aura import VisualAuraComponent
from in_game.ecs.components.occupier_component import OccupierComponent
from in_game.ecs.components.resource_component import ResourceComponent
from in_game.ecs.components.health_component import HealthComponent
from in_game.ecs.components.movement_component import MovementComponent
from in_game.map.tile import GameTile
from algorithms import hex_radius
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

            if sprite_component.image:
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
        event_bus.subscribe('entity_moved_to_tile', self.move_entity_to_tile)
        event_bus.subscribe('entity_dragged_to_tile', self.move_entity_to_tile)
        event_bus.subscribe('remove_entity_from_tile', self.remove_entity_from_tile)

    def draw_entity(self, display:pg.Surface, entity: Entity):
        sprite_component: Optional[SpriteComponent] = entity.get_component(SpriteComponent)
        position_component: ScreenPositionComponent = entity.get_component(ScreenPositionComponent)
        if sprite_component.is_visible and position_component.position:
            pos = self.get_top_left_position(sprite_component.image, position_component.position)
            pos = (pos[0], pos[1] - sprite_component.y_offset)
            display.blit(sprite_component.image, pos)

            if entity.has_component(ResourceComponent):
                self.draw_resource_component(
                    display, entity, sprite_component, pos
                )

            if entity.has_component(HealthComponent):
                self.draw_health_component(
                    display, entity, sprite_component, pos
                )

            #has health component
                
    def draw_resource_component(self, display: pg.Surface, entity: Entity,          sprite_component: SpriteComponent, pos: tuple[int,int]):
        y_pos = pos[1] - 3
        line_width = 4

        resource_component: ResourceComponent = entity.get_component(ResourceComponent)
        image_size = sprite_component.image.get_size()
        left_pos = (pos[0] + 20, y_pos)
        right_pos = (pos[0] + image_size[0] - 20, y_pos)
        pg.draw.line(display, (210, 212, 212), left_pos, right_pos, line_width)

        perc_of_resource =  resource_component.amount / resource_component.max
        bar_len = right_pos[0] - left_pos[0]
        line_length = int(perc_of_resource*bar_len)
        x_pos = left_pos[0] + line_length
        resource_pos = (x_pos, y_pos) 
        pg.draw.line(display, resource_component.color, left_pos, resource_pos, line_width)

    def draw_health_component(self, display: pg.Surface, entity: Entity,          sprite_component: SpriteComponent, pos: tuple[int,int]):
            health_component: HealthComponent = entity.get_component(HealthComponent)
            y_pos = pos[1] - 8
            line_width = 8
            health_color = (48, 184, 66)

            image_size = sprite_component.image.get_size()
            left_pos = (pos[0] + 20, y_pos)
            right_pos = (pos[0] + image_size[0] - 20, y_pos)
            pg.draw.line(display, (210, 212, 212), left_pos, right_pos, line_width)

            perc_of_resource =  health_component.current / health_component.max
            bar_len = right_pos[0] - left_pos[0]
            line_length = int(perc_of_resource*bar_len)
            x_pos = left_pos[0] + line_length
            resource_pos = (x_pos, y_pos) 
            pg.draw.line(display, health_color, left_pos, resource_pos, line_width)

    def entity_to_tile(self, tile: GameTile, entity: Entity):
        center_pixel = tile.center_pixel
        sprite_comp: SpriteComponent = entity.get_component(SpriteComponent)
        position_comp: ScreenPositionComponent = entity.get_component(ScreenPositionComponent)

        sprite_comp.is_visible = True
        position_comp.position = center_pixel

    def remove_entity_from_tile(self, entity: Entity, tile:GameTile):
        position_comp: ScreenPositionComponent = entity.get_component(ScreenPositionComponent)
        position_comp.position = None

    def move_entity_to_tile(self, entity:Entity, from_tile: GameTile, to_tile: GameTile):
        self.entity_to_tile(to_tile, entity)

class DrawMovementSystem(RenderSystem):
    required_components = [MovementComponent]

    def __init__(self, event_bus: EventBus) -> None:
        super().__init__(event_bus)

    def draw_entity(self, display: pg.Surface, entity: Entity):
        movement_comp: MovementComponent = entity.get_component(MovementComponent)

        if len(movement_comp.queue) > 0:
            line_points = [tile.center_pixel for tile in movement_comp.queue]
            line_points = [movement_comp.start_tile.center_pixel] + line_points

            if len(line_points) >= 2:
                pg.draw.lines(display, movement_comp.line_color, False, line_points,  movement_comp.line_width)
       

class DrawHexEdgeSystem(RenderSystem):
    required_components = [VisualHexEdgeComponent, ScreenPositionComponent]

    def __init__(self, event_bus: EventBus) -> None:
        super().__init__(event_bus)
        self.event_bus.subscribe('idle_enter', self.reset_all_edges)
        self.event_bus.subscribe('tile_in_movement_range', self.update_tiles_in_movement_range)

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

    def update_tiles_in_movement_range(self, tiles: set[GameTile]):
        self.reset_all_edges()
        for tile in tiles:
            visual_edge_comp: VisualHexEdgeComponent = tile.get_component(VisualHexEdgeComponent)
            visual_edge_comp.thickness = 2
            visual_edge_comp.color = (255, 255, 255)

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
        if not self.action_state.is_spawning:
            for entity in self.entities:
                self.draw_entity(display, entity)

    def draw_entity(self, display:pg.Surface, tile: GameTile):
        visual_component: Optional[SelectedHexEdgeComponent] = tile.get_component(SelectedHexEdgeComponent)
        if visual_component:
            pg.draw.polygon(display, visual_component.color, visual_component.verticies, visual_component.thickness)

    
class DrawFogOfWarSystem(RenderSystem):
    required_components = [TileSpriteComponent, FogOfWarComponent, ScreenPositionComponent]

    def draw(self, display: pg.Surface):
        trans_surface = pg.Surface(display.get_size(), pg.SRCALPHA)
        for entity in self.entities:
            fog_of_war_comp: FogOfWarComponent = entity.get_component(FogOfWarComponent)
            if fog_of_war_comp.is_fog_of_war:
                sprite_component: TileSpriteComponent = entity.get_component(TileSpriteComponent)

                pg.draw.polygon(trans_surface, (0, 0, 0, 100), sprite_component.verticies)
        display.blit(trans_surface, (0,0))

    def draw_entity(self, display: pg.Surface, entity: Entity):
        ...

class DrawFogOfWarSystem(RenderSystem):
    required_components = [FogOfWarComponent, TileSpriteComponent]

    def draw(self, display: pg.Surface):
        trans_surface = pg.Surface(display.get_size(), pg.SRCALPHA)
        for entity in self.entities:
            fog_of_war_comp: FogOfWarComponent = entity.get_component(FogOfWarComponent)
            if fog_of_war_comp.is_fog_of_war:
                sprite_component: TileSpriteComponent = entity.get_component(TileSpriteComponent)

                pg.draw.polygon(trans_surface, (0, 0, 0, 100), sprite_component.verticies)
        display.blit(trans_surface, (0,0))

    def draw_entity(self, display: pg.Surface, entity: Entity):
        ...


class DrawAuraSystem(RenderSystem):
    required_components = [VisualAuraComponent, OccupierComponent]

    def draw_entity(self, display: pg.Surface, entity: Entity):
        trans_surface = pg.Surface(display.get_size(), pg.SRCALPHA)
        visual_aura_comp: VisualAuraComponent = entity.get_component(VisualAuraComponent)
        occupier_component: OccupierComponent = entity.get_component(OccupierComponent)
        
        if len(occupier_component.tiles) > 0:
            for tile in occupier_component.tiles:
                tiles_in_aura = hex_radius(tile, visual_aura_comp.radius)

                for aura_tile in tiles_in_aura:
                    distance_from = tile.distance_to(aura_tile)

                    tapering_intensity = 1 - (distance_from * visual_aura_comp.tapering_intensity)
                    
                    alpha = int(tapering_intensity * visual_aura_comp.transparency_value)
                   
                    color = visual_aura_comp.color[:3] + (alpha,)
                    pg.draw.polygon(trans_surface, color, aura_tile.verticies)

        display.blit(trans_surface, (0,0))

    




    


