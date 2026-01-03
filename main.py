import random
import numpy as np
from leap_ec import Individual, representation
from leap_ec.problem import ScalarProblem
from container import Container, ContainerType, CONTAINER_SIZES
from area import Area
from plot_layouts import plot_layout

class LayoutDecoder:
    def __init__(self, area, spacing=0.1, step=0.1):
        self.area = area
        self.spacing = spacing
        self.step = step
        # granice area
        xs = [p[0] for p in area.polygon]
        ys = [p[1] for p in area.polygon]
        self.min_x, self.max_x = min(xs), max(xs)
        self.min_y, self.max_y = min(ys), max(ys)

    def decode(self, genome):
        containers = []
        cid = 1
        # Genome struktura: [type_1, rot_1, type_2, rot_2, ...] dzieli na pojedyncze geny 
        genes = [genome[i:i + 2] for i in range(0, len(genome), 2)]
        gene_idx = 0
        
        types = list(ContainerType)
        y = self.min_y + self.spacing
        
        # stawia linia po lini
        while y <= self.max_y - self.spacing:
            x = self.min_x + self.spacing
            row_max_h = 0 
            
            while x <= self.max_x - self.spacing:
                current_gene_pair = genes[gene_idx % len(genes)]
                type_gene, rot_gene = current_gene_pair
                gene_idx += 1
                
                t_idx = int(type_gene * (len(types) - 1))
                ctype = types[t_idx]
                w, h = CONTAINER_SIZES[ctype.value]

                if rot_gene > 0.5:
                    w, h = h, w

                if x + w <= self.max_x - self.spacing and y + h <= self.max_y - self.spacing:
                    new_c = Container(cid, ctype, x, y, w, h)
                    containers.append(new_c)
                    cid += 1
                    
                    x += w + self.spacing
                    row_max_h = max(row_max_h, h)
                else:
                    x += self.step
            
            if gene_idx >= len(genes): break
            y += (row_max_h + self.spacing) if row_max_h > 0 else self.step
            
        return containers



class ContainerPlacementProblem(ScalarProblem):
    def __init__(self, decoder):
        super().__init__(maximize=True) 
        self.decoder = decoder

    def evaluate(self, genome):
        """
        do zaimplementowania fitnes
        najwazniejsze jest karanie gdyby containers na siebie nachodziły 
        mona tez ustalić jakies proporcje typów containers do siebie 
        (np co najmiej jeden sanitary na dwa residential)
        """
        containers = self.decoder.decode(genome)
        return len(containers)


if __name__ == "__main__":
    #typ Area - na razie same regularne
    area = Area.rectangular(10, 8)
    max_potential_containers = 200
    genome_length = max_potential_containers * 2
    
    decoder = LayoutDecoder(area)
    problem = ContainerPlacementProblem(decoder)

    # pierwsza generacja
    initial_genome = [random.random() for _ in range(genome_length)]
    
    # wstępny fitnes (zliczanie ilości containers)
    fitness = problem.evaluate(initial_genome)
    print(f"Initial Layout Fitness (Count): {fitness}")

    #wizualizacja
    layout_containers = decoder.decode(initial_genome)
    plot_layout(area, layout_containers, f"Layout (Count: {len(layout_containers)})")