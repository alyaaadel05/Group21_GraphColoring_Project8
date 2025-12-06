import random
import time
from . import utils

# --- TIBAH ---
DEFAULT_PARAMS = {
    "population_size": 50,
    "generations": 200,
    "mutation_rate": 0.1,
    "crossover_rate": 0.9,
    "elite_fraction": 0.1,
    "belief_influence": 0.7,
    "tournament_size": 3,
    "random_seed": None,
}

# --- AYA ---
def solve_cultural(adj, k, params=None):
    cfg = DEFAULT_PARAMS.copy()
    if params:
        cfg.update(params)

    pop_size = cfg["population_size"]
    max_generations = cfg["generations"]
    mutation_rate = cfg["mutation_rate"]
    crossover_rate = cfg["crossover_rate"]
    elite_fraction = cfg["elite_fraction"]
    belief_influence = cfg["belief_influence"]
    tournament_size = cfg["tournament_size"]
    seed = cfg["random_seed"]

    if seed is not None:
        random.seed(seed)

    n = len(adj)
    start_time = time.perf_counter()

    # --- AYA ---
    def evaluate_coloring(coloring):
        res = utils.check_coloring(adj, coloring, k)
        if isinstance(res, tuple) and len(res) == 2:
            is_valid, conflicts = res
        elif isinstance(res, bool):
            is_valid = res
            conflicts = 0 if res else _compute_conflicts_from_adj(coloring)
        else:
            conflicts = int(res)
            is_valid = (conflicts == 0)
        return conflicts, is_valid

    # --- AYA ---
    def _compute_conflicts_from_adj(coloring):
        conflicts = 0
        for u in range(n):
            cu = coloring[u]
            for v in adj[u]:
                if v > u and coloring[v] == cu:
                    conflicts += 1
        return conflicts

    # --- AYA ---
    def random_coloring():
        return [random.randrange(k) for _ in range(n)]

    # --- AYA ---
    def initialize_population():
        return [random_coloring() for _ in range(pop_size)]

    # --- AYA ---
    def tournament_select(population, fitnesses):
        best_idx = random.randrange(len(population))
        best_fit = fitnesses[best_idx]
        for _ in range(tournament_size - 1):
            idx = random.randrange(len(population))
            if fitnesses[idx] < best_fit:
                best_idx = idx
                best_fit = fitnesses[idx]
        return population[best_idx]

    # --- AYA ---
    def crossover(parent1, parent2):
        if random.random() > crossover_rate or n <= 1:
            return parent1[:], parent2[:]
        point = random.randint(1, n - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    # --- TIBAH ---
    normative = [set(range(k)) for _ in range(n)]
    situational = None

    # --- TIBAH ---
    def update_belief_space(population, fitnesses):
        nonlocal situational, normative
        idxs = list(range(len(population)))
        idxs.sort(key=lambda i: fitnesses[i])
        elite_count = max(1, int(elite_fraction * len(population)))
        elite_idxs = idxs[:elite_count]
        best_idx = idxs[0]
        best_fit = fitnesses[best_idx]
        best_col = population[best_idx]
        if situational is None or best_fit < situational[1]:
            situational = (best_col[:], best_fit)
        new_normative = [set() for _ in range(n)]
        for i in elite_idxs:
            col = population[i]
            for v in range(n):
                new_normative[v].add(col[v])
        for v in range(n):
            if new_normative[v]:
                normative[v] = new_normative[v]

    # --- TIBAH ---
    def mutate(coloring):
        for v in range(n):
            if random.random() < mutation_rate:
                if random.random() < belief_influence and normative[v]:
                    choices = list(normative[v])
                else:
                    choices = list(range(k))
                current = coloring[v]
                if len(choices) > 1 and current in choices:
                    choices.remove(current)
                coloring[v] = random.choice(choices)
        return coloring

    # --- AYA ---
    population = initialize_population()
    best_coloring = None
    best_fitness = float("inf")
    generations_used = 0

    # --- AYA + TIBAH (shared loop, Aya controls GA, Tibah controls belief updates) ---
    for gen in range(max_generations):
        generations_used = gen + 1
        fitnesses = []
        for ind in population:
            fit, is_valid = evaluate_coloring(ind)
            fitnesses.append(fit)
            if fit < best_fitness:
                best_fitness = fit
                best_coloring = ind[:]
        update_belief_space(population, fitnesses)
        if best_fitness == 0:
            break
        idxs = list(range(len(population)))
        idxs.sort(key=lambda i: fitnesses[i])
        elite_count = max(1, int(elite_fraction * pop_size))
        new_population = [population[i][:] for i in idxs[:elite_count]]
        while len(new_population) < pop_size:
            p1 = tournament_select(population, fitnesses)
            p2 = tournament_select(population, fitnesses)
            c1, c2 = crossover(p1, p2)
            c1 = mutate(c1)
            if len(new_population) < pop_size:
                new_population.append(c1)
            if len(new_population) < pop_size:
                c2 = mutate(c2)
                new_population.append(c2)
        population = new_population

    # --- AYA ---
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    nodes_explored = generations_used * pop_size

    if best_coloring is None and population:
        fitnesses = [evaluate_coloring(ind)[0] for ind in population]
        best_idx = min(range(len(population)), key=lambda i: fitnesses[i])
        best_coloring = population[best_idx][:]

    return {
        "coloring": best_coloring,
        "nodes_explored": nodes_explored,
        "backtracks": 0,
        "time_ms": elapsed_ms,
    }
