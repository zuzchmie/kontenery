from enum import Enum
import math

CONTAINER_SIZES = {
    "residential": (1.0, 0.5),
    "kitchen": (1.0, 0.5),
    "sanitary": (0.5, 0.5),
    "common": (1.5, 1.0)
}

class ContainerType(Enum):
    RESIDENTIAL = "residential"
    KITCHEN = "kitchen"
    SANITARY = "sanitary"
    COMMON = "common"

class Container:
    def __init__(self, cid, ctype, x, y, width, height):
        self.id = cid
        self.type = ctype
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def polygon(self, angle_degrees=0):
        """Returns 4 vertices rotated around the origin (x, y)."""
        rad = math.radians(angle_degrees)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        local = [(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)]
        return [(lx * cos_a - ly * sin_a + self.x, lx * sin_a + ly * cos_a + self.y) for lx, ly in local]

    def center(self):
        return (self.x + self.width / 2, self.y + self.height / 2)