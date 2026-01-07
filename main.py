import random
import numpy as np
from leap_ec import Individual, representation
from leap_ec.problem import ScalarProblem
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
        # definiuje początkowy kąt - na razie ranodmo z ewolucja powinnien sie dopasowywać
        global_angle = genome[0] * 90
        containers = []
        cid = 1
        
        # dzielenie genomy n amniejsze geny
        # Genome struktura: [type_1, rot_1, type_2, rot_2, ...]
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
                #wciąz obracanie o 90 stopni
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
        score = len(containers)
        
        return float(score)

if __name__ == "__main__":
    
    area = Area.wedge_poly()
    
    pattern_size = 50
    genome_length = 1 + (pattern_size * 2)
    
    decoder = LayoutDecoder(area, spacing=0.1, step=0.2)
    problem = ContainerPlacementProblem(decoder)

    
    initial_genome = [random.random() for _ in range(genome_length)]
    
    layout_containers, final_angle = decoder.decode(initial_genome)
    
    fitness = problem.evaluate(initial_genome)
    print(f"Containers: {len(layout_containers)}")

    plot_layout(area, layout_containers, f"Layout (Containers: {len(layout_containers)})", global_angle=final_angle)