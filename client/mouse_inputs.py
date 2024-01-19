from abc import ABC

class MouseInput(ABC):  
    def __init__(self, pixel):
        self.pixel = pixel

class Click(MouseInput):
    def __init__(self, pixel):
        super().__init__(pixel)

class DragStart(MouseInput):
    def __init__(self, pixel):
        super().__init__(pixel)

class Dragging(MouseInput):
    def __init__(self, pixel):
        super().__init__(pixel)

class DragEnd(MouseInput):
    def __init__(self, pixel):
        super().__init__(pixel)



    
