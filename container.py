from enum import Enum

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

    def polygon(self):
        return [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width, self.y + self.height),
            (self.x, self.y + self.height)
        ]

    def center(self):
        return (
            self.x + self.width / 2,
            self.y + self.height / 2
        )
