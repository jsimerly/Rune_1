from math import sqrt


class Orientation:
    def __init__(self, f0, f1, f2, f3, b0, b1, b2, b3, start_angle) -> None:
        '''
        f values- are used to convert the 3D cordinates to 2D (forward)
        b values- are used to convert the 2D cordinates to 3D (backwards)
        '''

        self.f0 = f0
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.start_angle = start_angle

orientation_pointy = Orientation(
        sqrt(3), sqrt(3)/2, 0, 3/2,
        sqrt(3)/3, -1/3, 0, 2/3,
        30
    )

orientation_flat = Orientation(
    3/2, 0, sqrt(3)/2, sqrt(3),
    2/3, 0, -1/3, sqrt(3)/3,
    0.0
)