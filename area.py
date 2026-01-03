class Area:
    def __init__(self, polygon):
        self.polygon = polygon

    @staticmethod
    def rectangular(width, height):
        return Area([(0, 0), (width, 0), (width, height), (0, height)])

    @staticmethod
    def rhombus(width, height, offset):
        return Area([(0, 0), (width, 0), (width + offset, height), (offset, height)])

    @staticmethod
    def irregular_quadrilateral():
        """A 4-sided polygon where no two sides are parallel."""
        return Area([
            (0, 0),    # Bottom-left
            (11, 1),   # Bottom-right (slight uphill slope)
            (9, 7),    # Top-right (inward tilt)
            (1, 8)     # Top-left (steeper height than bottom-left)
        ])

    @staticmethod
    def jagged_pentagon():
        """A 5-sided irregular shape with varying angles."""
        return Area([
            (0, 2),    # Left start
            (5, 0),    # Bottom peak
            (12, 3),   # Right stretch
            (10, 9),   # Top-right
            (2, 7)     # Top-left
        ])

    @staticmethod
    def wedge_poly():
        """A 6-sided 'wedge' shape with non-parallel segments."""
        return Area([
            (0, 0), (8, 1), (12, 5), (9, 10), (3, 8), (1, 4)
        ])