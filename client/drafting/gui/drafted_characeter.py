import pygame as pg

class DraftedCharacter:
    def __init__(self, position: (int, int, int)):
        self.size = (150, 150)
        self.image = None
        self.is_active = False
        self.is_next = False
        self.rect = pg.Rect(position, self.size)
        self.outline_color = (149, 220, 252)

    def set_image(self, image: pg.Surface):
        self.image = image

    def set_is_active(self):
        self.is_next = False
        self.is_active = True

    def set_is_next(self):
        self.is_next = True

    def set_pick(self):
        self.is_active = False
        self.is_picked = True

    def draw(self, display: pg.Surface):
        if self.image:
            display.blit(self.image, self.rect)
            
        if self.is_active:
            pg.draw.rect(display, self.outline_color, self.rect, 8)

        if self.is_next:
            pg.draw.rect(display, self.outline_color, self.rect, 3)
        
        if all([
            not self.is_active,
            not self.is_next,
        ]):
            pg.draw.rect(display, self.outline_color, self.rect, 3)



class BannedCharacter(DraftedCharacter):
    def __init__(self, position: (int, int, int)):
        super().__init__(position)
        self.outline_color = (168, 10, 10)
