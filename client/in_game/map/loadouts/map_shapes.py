from typing import Tuple, List

def hexagon(radius:int) -> List[Tuple[int,int]]:
    if radius < 1:
        raise ValueError('radius of hexagon must be greater than 0')
    radius -= 1
    offset = 1
    hexes = []
    for q in  range(-radius, radius + offset):
        r1 = max(-radius, -q - radius)
        r2 = min(radius, -q + radius) + offset
        for r in range(r1,r2):
            hex = (q, r)
            hexes.append(hex)
    return hexes