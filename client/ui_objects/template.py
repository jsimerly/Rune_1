from ui_objects.abs_ui_object import AbsButton
import pygame as pg

class TextButton(AbsButton):
    def __init__(self, rect: pg.Rect, text, text_color, color, outline=None, text_size:int=None):
        super().__init__(rect)
        self.text = text
        self.text_color = text_color
        self.color = color
        self.outline_colors = outline

        pg.font.init()
        if text_size == None:
            text_size = 20
        self.font = pg.font.SysFont(None, text_size)

    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, self.color, self.rect)
        if self.outline_colors:
            pg.draw.rect(screen, self.outline_colors, self.rect, 1)

        text_surface = self.font.render(self.text, True, self.text_color)
        point = self.rect.center
        text_pos = (point[0] - text_surface.get_width() // 2, point[1] - text_surface.get_height() // 2)
        screen.blit(text_surface, text_pos)
        
    def on_click(self):
        ...