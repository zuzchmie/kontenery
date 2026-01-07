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
        return Area([
            (0, 0),    
            (11, 1),   
            (9, 7),    
            (1, 8)     
        ])

    @staticmethod
    def jagged_pentagon():
        return Area([
            (0, 2),    
            (5, 0),    
            (12, 3),   
            (10, 9),   
            (2, 7)     
        ])

    @staticmethod
    def wedge_poly():
        return Area([
            (0, 0), (8, 1), (12, 5), (9, 10), (3, 8), (1, 4)
        ])