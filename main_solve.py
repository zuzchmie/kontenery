import random
import math
import numpy as np
from leap_ec.problem import ScalarProblem
from leap_ec.simple import ea_solve
from container import Container, ContainerType, CONTAINER_SIZES
from area import Area
from plot_layouts import plot_layout

class LayoutDecoder:
    def __init__(self, area, spacing=0.1, step=0.2):
        self.area = area
        self.spacing = spacing
        self.step = step
        xs, ys = zip(*area.polygon)
        self.min_x, self.max_x = min(xs), max(xs)
        self.min_y, self.max_y = min(ys), max(ys)

    def _project(self, poly, normal):
        dots = [p[0] * normal[0] + p[1] * normal[1] for p in poly]
        return min(dots), max(dots)

    def rotated_overlap(self, poly1, poly2):
        for poly in [poly1, poly2]:
            for i in range(len(poly)):
                p1, p2 = poly[i], poly[(i + 1) % len(poly)]
                normal = (-(p2[1] - p1[1]), p2[0] - p1[0])
                min1, max1 = self._project(poly1, normal)
                min2, max2 = self._project(poly2, normal)
                if max1 < min2 or max2 < min1:
                    return False
        return True

    def is_fully_contained(self, corners):
        for x, y in corners:
            inside = False
            n = len(self.area.polygon)
            p1x, p1y = self.area.polygon[0]
            for i in range(n + 1):
                p2x, p2y = self.area.polygon[i % n]
                if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
                p1x, p1y = p2x, p2y
            if not inside:
                return False
        return True

    def decode(self, genome):
        global_angle = genome[0] * 90
        containers = []
        cid = 1

        genes = [genome[i:i + 2] for i in range(1, len(genome), 2)]
        gene_idx = 0
        types = list(ContainerType)

        y = self.min_y - 2 
        while y <= self.max_y:
            x = self.min_x - 2
            row_max_h = 0
            placed_in_row = False
            
            while x <= self.max_x:
                pair = genes[gene_idx % len(genes)]
                gene_idx += 1
                
                t_idx = int(pair[0] * (len(types) - 1))
                ctype = types[t_idx]
                w, h = CONTAINER_SIZES[ctype.value]
                if pair[1] > 0.5:
                    w, h = h, w
                
                new_c = Container(cid, ctype, x, y, w, h)
                corners = new_c.polygon(global_angle)

                if self.is_fully_contained(corners):
                    collision = False
                    for existing in containers:
                        if self.rotated_overlap(corners, existing.polygon(global_angle)):
                            collision = True
                            break
                    
                    if not collision:
                        containers.append(new_c)
                        cid += 1
                        x += w + self.spacing
                        row_max_h = max(row_max_h, h)
                        placed_in_row = True
                    else:
                        x += self.step
                else:
                    x += self.step
            y += (row_max_h + self.spacing) if placed_in_row else self.step
            
        return containers, global_angle

class ContainerPlacementProblem(ScalarProblem):
    def __init__(self, decoder):
        super().__init__(maximize=True)
        self.decoder = decoder

    def evaluate(self, genome):
        containers, _ = self.decoder.decode(genome)

        if not containers:
            return -1e6

        res = [c for c in containers if c.type == ContainerType.RESIDENTIAL]
        kit = [c for c in containers if c.type == ContainerType.KITCHEN]
        san = [c for c in containers if c.type == ContainerType.SANITARY]
        com = [c for c in containers if c.type == ContainerType.COMMON]

        def dist(c1, c2):
            x1, y1 = c1.center()
            x2, y2 = c2.center()
            return math.hypot(x1 - x2, y1 - y2)

        def avg_dist(A, B):
            if not A or not B:
                return 50
            return sum(min(dist(a, b) for b in B) for a in A) / len(A)

        d_k = avg_dist(res, kit)
        d_s = avg_dist(res, san)
        d_c = avg_dist(res, com)

        area_box = (self.decoder.max_x - self.decoder.min_x) * \
                   (self.decoder.max_y - self.decoder.min_y)
        used = sum(c.width * c.height for c in containers)
        free_ratio = max(0, area_box - used) / area_box

        penalty = 0
        if not kit: penalty += 50
        if not san: penalty += 80
        if not com: penalty += 30
        if free_ratio < 0.15: penalty += 40

        return (
            10 * len(res)
            - 2 * d_k
            - 3 * d_s
            - d_c
            + 20 * free_ratio
            - penalty
        )

if __name__ == "__main__":

    random.seed(42)
    np.random.seed(42)

    area = Area.jagged_pentagon()
    pattern_size = 50
    genome_length = 1 + pattern_size * 2

    decoder = LayoutDecoder(area)
    problem = ContainerPlacementProblem(decoder)

    bounds = [(0.0, 1.0)] * genome_length

    best_genome = ea_solve(
        problem.evaluate,  
        bounds=bounds,
        generations=300,
        pop_size=50,
        mutation_std=0.1,
        maximize=True,
        viz=False
    )

    containers, angle = decoder.decode(best_genome)

    best_fitness = problem.evaluate(best_genome)

    print("=== RESULT ===")
    print(f"Fitness: {best_fitness:.2f}")
    print(f"Containers: {len(containers)}")

    plot_layout(
        area,
        containers,
        "Best container layout",
        global_angle=angle
    )
