from __future__ import annotations
from math import sqrt, radians, cos, sin, pi
import pygame
from typing import List, Tuple


cube_direction_vectors = [
    (-1, 0, 1), (0, -1, 1), (1, -1, 0),
    (1, 0, -1), (0, 1, -1), (-1, 1, 0)
]
class Hex:
    def __init__(self, q:int, r:int, s:int = None) -> None:        
        #(q, r, s) 
        #Can be optimized by switching the a list function to run multithreaded once we move to C#
        if s is None:
            s = -q - r
        if q + r + s != 0:
            raise ValueError("Error: q + r + s must equal 0.")
        
        self.q = q
        self.r = r
        self.s = s

    def __eq__(self, other) -> bool:
        if isinstance(other, Hex):
            return all([
                self.q == other.q,
                self.r == other.r,
                self.s == other.s
            ])
        return False
    
    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
    
    def __add__(self, other) -> Hex:
        if isinstance(other, Hex):
            return Hex(self.q + other.q, self.r + other.r, self.s + other.s)

        if isinstance(other, tuple) and len(other) == 3:
            return Hex(self.q + other[0], self.r + other[1], self.s + other[2])

        return NotImplemented

    def __sub__(self, other) -> Hex:
        if isinstance(other, Hex):
            return Hex(self.q - other.q, self.r - other.r, self.s - other.s)

        if isinstance(other, tuple) and len(other) == 3:
            return Hex(self.q - other[0], self.r - other[1], self.s - other[2])

        return NotImplemented
    
    def __mul__(self, other) -> Hex:
        if isinstance(other, Hex):
            return Hex(self.q * other.q, self.r * other.r, self.s * other.s)

        if isinstance(other, (int, float)):
            #Other = k when it's a scalar value
            return Hex(self.q * other, self.r * other, self.s * other)
        
        if isinstance(other, tuple) and len(other) == 3:
            return Hex(self.q * other[0], self.r * other[1], self.s * other[2])
        
        return NotImplemented
    
    def __hash__(self) -> (int, int):
        return hash((self.q, self.r))
    
    @property
    def axial(self):
        return (self.q, self.r)
    
    def magnitude(self, other=None) -> int:
        ''' We divide by two because we're using a 3D grid system with a plane through it at x + y + z = 0.
        Typically, in a 3D system, we would calculate the length of this vector using the distance from 0, 0, 0.
        But, because we're only using diagnols, as opposed to every block in a discrete 3D grid, that means we're
        double counting using Manhattan distances. '''
        hex = self if other is None else other

        return int((abs(hex.q) + abs(hex.r) + abs(hex.s))/2)
    
    def distance_to(self, other) -> int:
        return self.magnitude(self-other)
    
    def direction(self, direction) -> (int, int, int):
        if -6 <= direction <= 5:
            return cube_direction_vectors[direction]
        raise ValueError("direction must be between -5 to 5")
    
    def neighbor(self, direction) -> Hex:
        return self + self.direction(direction)
    
    def get_all_neighors(self) -> List[Hex]:
        neighbors = []
        for i in range(6):
            neighbors.append(self.neighbor(i))
        return neighbors
    
    def lerp(a: float, b:float, t:float) -> float:
        return a * (1-t) + (b * t)
        # a + (b - a) * t is more recognizable but worse on floating point arithmetic
    
    def hex_lerp(self, target_hex, t) -> Hex:
        if isinstance(target_hex, Hex):
            return fractional_to_int_hex(
                    self.lerp(self.q, target_hex.q, t),
                    self.lerp(self.r, target_hex.r, t),
                    self.lerp(self.s, target_hex.s, t)
                )
        raise ValueError("target_hex must be a Hex object.")
    
    #if this isn't working as intended, it may be due to exact values and we need a nudge
    def hex_line_to(self, target_hex:Hex) -> List[Hex]:
        N = self.distance_to(target_hex)
        hexes = []
        for i in range(N):
            hex = self.hex_lerp(target_hex, 1.0/N * i)
            hexes.append(hex)
        return hexes

    def rotate(self, n_rotations:int, origin, counter=False) -> Hex:
        radius = self.distance_to(origin)
        hex = Hex(*cube_direction_vectors[0]) * radius #starting hex to start the search for self

        rotation_count = 0
        found = False
        rotation_range = range(-5,1) if counter else range(6)
        for i in rotation_range:
            for _ in range(radius):
                hex=hex.neighbor(i)

                if found:
                    rotation_count += 1
                    if rotation_count == n_rotations:
                        self.q = hex.q
                        self.r = hex.r
                        self.s = hex.s
                        return self

                if hex == self:
                    found = True

    def rotate_60(self, counter=False) -> Hex:
        q = self.q
        r = self.r
        s = self.s

        if counter:
            self.q = -s
            self.r = -q
            self.s = -r
        else:
            self.q = -r
            self.r = -s
            self.s = -q
        return self
    
    def rotate_60_n(self, n_rotations, counter=False) -> Hex:
        n_rotations %= 6
        for _ in range(n_rotations):
            self.rotate_60(counter)
        return self
       

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

#Could use (x, y) to reduce memory over head if needed. The added methods may not be that useful.
Point = pygame.math.Vector2

def fractional_to_int(q1: float, r1: float, s1: float) -> (int, int, int):
    q = int(round(q1))
    r = int(round(r1))
    s = int(round(s1))

    dq = abs(q1-q)
    dr = abs(r1-r)
    ds = abs(s1-s)

    if (dq > dr and dq > ds):
        q = -r -s        
    elif (dr > ds):
        r = -q -s
    else:
        s = -q -r

    return (q, r, s)

def fractional_to_int_hex(q1: float, r1: float, s1: float) -> (int, int, int):
    return Hex(fractional_to_int(q1, r1, r1))

class Layout:
    def __init__(self, orientation: Orientation, size, origin, skew: int=0) -> None:
        self.orientation = orientation
        self.size = size
        self.origin = origin
        self.skew = skew

    #returns the center of the hex
    def hex_to_pixel(self, hex: Hex) -> (int, int): 
        M = self.orientation # M is the matrix for the orientation
        x = (M.f0 * hex.q + M.f1 * hex.r) * self.size[0]
        y = (M.f2 * hex.q + M.f3 * hex.r) * self.size[1]
        return (x + self.origin[0], y + self.origin[1])
    
    #returns a floating hex location that needs to be converted to target an real hex
    def pixel_to_hex_coord(self, pixel_pos) -> Hex:
        M = self.orientation
        x, y = pixel_pos
        pt_x = (x - self.origin.x) / self.size.x
        pt_y = (y - self.origin.y) / self.size.y

        q1 = M.b0 * pt_x + M.b1 * pt_y
        r1 = M.b2 * pt_x + M.b3 * pt_y
        s1 = -q1 - r1

        return fractional_to_int(q1, r1, s1)
    
    def pixel_to_hex(self, pixel_pos):
        coords = self.pixel_to_hex_coord(pixel_pos)
        return Hex(coords)
    

    
    def get_corner_offset(self, corner: int) -> (int, int):
        angle_deg = 60 * corner + self.orientation.start_angle
        angle_rad = radians(angle_deg)
        x = self.size[0] * cos(angle_rad)
        y = self.size[1] * sin(angle_rad)

        x += self.skew * y
        return (x, y)
    
    def get_hex_verticies(self, p: Point) -> List[(int, int)]:
        verticies = []
        for corner in range(6):
            offset = self.get_corner_offset(corner)
            vertex = (p[0] + offset[0], p[1] + offset[1])
            verticies.append(vertex)
        return verticies
    
    def parallelogram(self, width: Tuple[int, int], height: Tuple[int,int], shape:str) -> List[Hex]:
        if shape not in ['skew-left', 'diamond', 'skew-right']:
            raise ValueError('parallelograms shape need to be either "skew-left", "diamond", or "skew-right"')
        
        #could be quicker if I put logic check outside but this is cleaner and shouldn't cause performance issues.
        hexes = []
        for i in range(width[0], width[1]):
            for j in range(height[0], height[1]):
                if shape == 'skew-left':
                    hex = Hex(i, j, -i-j)
                if shape == 'diamond':
                    hex = Hex(j, -i-j, i)
                if shape == 'skew-right':
                    hex = Hex(-i-j, j, i)
                hexes.append(hex)
        return hexes
    
    def triangle(self, edge_length:int, orientation:str) -> List[Hex]:
        if orientation not in ['top', 'bottom']:
            raise ValueError('triangle orientation needs to be either "top" or "bottom"')

        hexes = []
        if orientation == 'bottom':
            for q in range(0, edge_length):
                for r in range(0, edge_length - q):
                    hex = Hex(q, r, -q-r)
                    hexes.append(hex)
        elif orientation == 'top':
            for q in range(0, edge_length):
                for r in range(0, q + 1):
                    hex = Hex(q, -q + r, -r)
                    hexes.append(hex)
        return hexes
    
    def hexagon(self, radius:int, tri_center:bool=False) -> List[Hex]:
        if radius < 1:
            raise ValueError('radius of hexagon must be greater than 0')
        hexes = []
        #radius is subtracted by 1 to make inputs more intuitive for size
        radius -= 1
        #offset is used if I want the center to be 3 hexagons instead of a central single hexagon.
        offset = 2 if tri_center else 1
        for q in range(-radius, radius + offset):
            r1 = max(-radius, -q - radius)
            r2 = min(radius, -q + radius) + offset
            for r in range(r1,r2):
                hex = Hex(q, r, -q-r)
                hexes.append(hex)
        return hexes
    
    def oblong(self, height:int, width:int) -> List[Hex]:
        hexes = []

        x_diff = height - width
        diff_range = range(height - abs(x_diff) + 1, height + 1)

        for q in range(-height, height + 1):
            r1 = max(-height, -q - height)
            r2 = min(height, -q + height) + 1

            if x_diff > 0:
                for r in range(r1, r2):
                    s = -q-r
                    if abs(q) in diff_range or abs(s) in diff_range:
                        continue
                    hex = Hex(q, r, -q-r)
                    hexes.append(hex)
            else:
                for r in range(r1, r2):
                    s = -q-r
                    if abs(r) in diff_range:
                        continue
                    hex = Hex(q, r, -q-r)
                    hexes.append(hex)

        return hexes
                               
    
    def tri(self, radius:int) -> List[Hex]:
        hexes = []

        for n in range(radius):
            hex1 = Hex(0, -n, n)
            hex2 = Hex(n, 0, -n)
            hex3 = Hex(-n, n, 0) 

            hexes.extend((hex1, hex2, hex3))

        return hexes
    
    #this in theory is possible to scale using triginometric interpolation, but it likely won't be used. If I need it in the future I will build it.
    def swirl_3(self, left_swirl=True) -> List[Hex]:
        hexes = []

        b=0
        for n in range(3):
            if n > 1:
                b = 1

            if left_swirl:
                hex1 = Hex(0-b, -n+b, n)
                hex2 = Hex(n, 0-b, -n+b)
                hex3 = Hex(-n+b, n, 0-b)
            else:
                hex1 = Hex(0+b, -n, n-b)
                hex2 = Hex(n-b, 0+b, -n)
                hex3 = Hex(-n, n-b, 0+b)

            hexes.extend((hex1, hex2, hex3))

        return hexes

    def ring(self, radius):
        if radius < 1:
            raise ValueError('ring radius needs to be greater than 1')
        hexes = []
        radius -= 1 #to make it more intuitive when using the function for abilities
        hex = Hex(*cube_direction_vectors[0]) * radius

        for i in range(6):
            for _ in range(radius): 
                hexes.append(hex)
                hex = hex.neighbor(i)
        return hexes
    
    def half_ring(self):
        pass
    
    def rectangle(self, width:int, height:int, odd=False) -> List[Hex]:
        hexes = []
        for r in range(height):
            # Adjust the offset for each row based on the stagger type
            r_offset = r // 2 if odd else (r + 1) // 2

            for q in range(-r_offset, width - r_offset):
                hex = Hex(q, r, -q - r)
                hexes.append(hex)
        return hexes

    def trapazoid(self, top_length:int, bottom_length:int, height:int) -> List[Hex]:
        if top_length > bottom_length:
            raise ValueError("Top length must be less than or equal to bottom length")
        
        hexes = []
        dw =  bottom_length - top_length
        start_q = -dw // 2

        for row in range(height):
            row_length = top_length + min(row, dw)

            for col in range(row_length):
                q = start_q + col
                r = row
                hex = Hex(q, r, -q-r)
                hexes.append(hex)

            if row < dw:
                start_q -= 1
        return hexes


    #maybe add this later
    def snowflake(self):
        pass
 
    



  
                
        
        
        



    
    




    

