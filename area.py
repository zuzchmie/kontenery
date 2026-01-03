class Area:
    def __init__(self, polygon):
        self.polygon = polygon

    @staticmethod
    def rectangular(width, height):
        return Area([
            (0, 0),
            (width, 0),
            (width, height),
            (0, height)
        ])


