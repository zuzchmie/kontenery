import random
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from area import Area
from main_solve import LayoutDecoder, ContainerPlacementProblem
from leap_ec.simple import ea_solve
from plot_layouts import plot_layout
import os

if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
    results=[]

    areas = [
        ('Pentagon', Area.jagged_pentagon()),
        ('Quadrilateral', Area.irregular_quadrilateral()),
        ('Wedge', Area.wedge_poly())
    ]

    for i in [100, 200]:
        for j in [100, 300]:
            for k in [1, 3]:
                for name, area1 in areas:
                    for spacing in [0.1, 0.3]:
                        for repeat in range (3):
                            folder = f"results/{name}/spacing_{spacing}/"
                            os.makedirs(folder, exist_ok=True)

                            pattern_size = 50
                            genome_length = 1 + pattern_size * 2

                            decoder = LayoutDecoder(area1, spacing=spacing, step=0.5)
                            problem = ContainerPlacementProblem(decoder)

                            bounds = [(0.0, 1.0)] * genome_length

                            best_genome = ea_solve(
                                problem.evaluate,
                                bounds=bounds,
                                generations=i,
                                pop_size=j,
                                mutation_std=k/10,
                                maximize=True,
                                viz=False
                            )

                            containers1, angle = decoder.decode(best_genome)
                            best_fitness = problem.evaluate(best_genome)

                            print("=== RESULT ===")
                            print(f"Fitness: {best_fitness:.2f}")
                            print(f"Containers: {len(containers1)}")

                            results.append({
                                'Generations': i,
                                'Population': j,
                                'Mutation_Std': k / 10,
                                'Fitness': best_fitness,
                                'Module_Count': len(containers1),
                                'Spacing': spacing,
                                'Area_Name': name
                            })

                            plot_layout(
                                area1,
                                containers1,
                                "Best container layout",
                                global_angle=angle,
                                name=folder+'layout '+'gen - '+str(i)+', pop - '+str(j)+', mutation - '+str(k)+', repeat - '+str(repeat)
                            )

    df = pd.DataFrame(results)
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='Generations', y='Fitness', hue='Area_Name')
    plt.savefig('boxplot'+".png")