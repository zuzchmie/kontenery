import csv
import itertools
import random
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

import numpy as np

from leap_ec.algorithm import generational_ea
from leap_ec.representation import Representation
from leap_ec import ops
from leap_ec.real_rep.ops import mutate_gaussian

from area import Area
from main_generational import LayoutDecoder, ContainerPlacementProblem


AREA = "wedge_poly"
PATTERN_SIZE = 50
REPEATS = 3
SEED = 42
OUT = "results/Grid Search/grid_search_results.csv"
MAX_COMBINATIONS = None

# Parameter grid to search over
GRID = {
    "pop_size": [30, 50],
    "max_generations": [50, 100],
    "mutation_std": [0.05, 0.1],
    "crossover_p_swap": [0.2, 0.5],
    "spacing": [0.1],
    "step": [0.1],
}


@dataclass(frozen=True)
class SearchConfig:
    pattern_size: int = 50
    max_generations: int = 200
    pop_size: int = 50
    mutation_std: float = 0.1
    crossover_p_swap: float = 0.5
    spacing: float = 0.1
    step: float = 0.2


def _build_area(name: str):
    name = name.strip().lower()
    if name == "wedge_poly":
        return Area.wedge_poly()
    if name == "jagged_pentagon":
        return Area.jagged_pentagon()



def run_one(cfg: SearchConfig, *, area_name: str, seed: int):
    random.seed(seed)
    np.random.seed(seed)

    area = _build_area(area_name)
    genome_length = 1 + cfg.pattern_size * 2

    decoder = LayoutDecoder(area, spacing=cfg.spacing, step=cfg.step)
    problem = ContainerPlacementProblem(decoder)

    pipeline = [
        ops.tournament_selection,
        ops.clone,
        mutate_gaussian(
            std=cfg.mutation_std,
            expected_num_mutations="isotropic",
            bounds=(0.0, 1.0),
        ),
        ops.UniformCrossover(p_swap=cfg.crossover_p_swap),
        ops.evaluate,
        ops.pool(size=cfg.pop_size),
    ]

    final_pop = generational_ea(
        max_generations=cfg.max_generations,
        pop_size=cfg.pop_size,
        problem=problem,
        representation=Representation(initialize=lambda: np.random.rand(genome_length)),
        pipeline=pipeline,
    )

    best = max(final_pop)
    containers, _ = decoder.decode(best.genome)
    return float(best.fitness), int(len(containers))


def iter_grid():
    keys = list(GRID.keys())
    for idx, values in enumerate(itertools.product(*[GRID[k] for k in keys])):
        if MAX_COMBINATIONS is not None and idx >= MAX_COMBINATIONS:
            return
        kwargs = dict(zip(keys, values))
        yield SearchConfig(**kwargs)


def main():
    out_path = Path(OUT)
    results = []
    best = None
    grid = list(iter_grid())
    total = len(grid)

    for idx, base_cfg in enumerate(grid, start=1):
        cfg = SearchConfig(
            pattern_size=PATTERN_SIZE,
            max_generations=base_cfg.max_generations,
            pop_size=base_cfg.pop_size,
            mutation_std=base_cfg.mutation_std,
            crossover_p_swap=base_cfg.crossover_p_swap,
            spacing=base_cfg.spacing,
            step=base_cfg.step,
        )

        fitnesses = []
        container_counts = []
        for rep in range(REPEATS):
            fitness, containers = run_one(cfg, area_name=AREA, seed=SEED + rep)
            fitnesses.append(fitness)
            container_counts.append(containers)

        mean_fit = float(np.mean(fitnesses))
        mean_cont = float(np.mean(container_counts))
        best_fit = float(np.max(fitnesses))

        row = {
            "mean_fitness": mean_fit,
            "best_fitness": best_fit,
            "mean_containers": mean_cont,
            "repeats": REPEATS,
            "area": AREA,
            **asdict(cfg),
        }
        results.append(row)

        if best is None or best_fit > best[0]:
            best = (best_fit, cfg, row)

        print(
            f"[{idx:>3}/{total}] mean={mean_fit:8.2f} best={best_fit:8.2f} "
            f"pop={cfg.pop_size} gen={cfg.max_generations} mut={cfg.mutation_std} "
            f"cx={cfg.crossover_p_swap}"
        )

    # Write results
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(results[0].keys()) if results else []
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


        print("\n=== Best fitness) ===")
        print(f"best_fitness: {best_fit:.2f}")


if __name__ == "__main__":
    main()
