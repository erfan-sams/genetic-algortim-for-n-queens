import random


## print final matrix
def matrix(list):
    for i in range(len(list)):
        for j in list:
            if j == i + 1:
                print('1', end='  ')
            else:
                print('0', end='  ')
        print()


## create random population
def random_individual(size):
    return [random.randint(1, size) for _ in range(size)]


## fitness function when fitness is 0 we have no collision and this is end:)
maxFitness = 28


def fitness(individual):
    """calculate collisions"""
    horizontal_collisions = sum([individual.count(queen) - 1 for queen in individual]) / 2

    """create list for observe diagonal collisions"""
    n = len(individual)
    left_diagonal = [0] * 2 * n
    right_diagonal = [0] * 2 * n
    for i in range(n):
        left_diagonal[i + individual[i] - 1] += 1
        right_diagonal[n - i + individual[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2 * n - 1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i] - 1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i] - 1
        diagonal_collisions += counter / (n - abs(i - n + 1))

    return int(maxFitness - (horizontal_collisions + diagonal_collisions))


""" pick element in population for next generation"""
def random_pick(population, probabilities,k):
    result = random.choices(population, weights=probabilities, k=k)
    if k == 2:
        return result[0], result[1]
    return result



def crossover(parent1, parent2):
    """take two parts for crossover and merge together"""
    n = len(parent1)
    crossover_index = random.randint(0, n)
    childrens = []
    first = parent1[0:crossover_index]
    first.extend(parent2[crossover_index:n])
    second = parent2[0:crossover_index]
    second.extend(parent1[crossover_index:n])
    childrens.append(first)
    childrens.append(second)
    return childrens


"""mutation change one element in list"""
def mutate(x):
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x


def generateNextPopulation(population, fitness):
    """mutation probability"""
    mutation_probability = 0.04
    new_population = []
    probabilities = [fitness(n) for n in population]
    """select random part for crossover"""
    new_population.extend(random_pick(population, probabilities,k=30))
    for i in range(int((len(population) - 30)/2)):
        x, y = random_pick(population, probabilities,k=2)
        childrens = crossover(x, y)
        new_population.extend(childrens)

    """ check for generate mutation"""
    for j in range(len(new_population)):
        if random.random() < mutation_probability:
            new_population[j] = mutate(new_population[j])
    return new_population


def final(size=8) -> None:
    """ main function get size and generate first population"""
    global maxFitness
    maxFitness = (size * (size - 1)) / 2
    population = [random_individual(size) for _ in range(100)]
    generation = 0
    while True:
        for x in population:
            if fitness(x) == maxFitness:
                print("Solved in Generation {}!".format(generation))
                print(x)
                matrix(x)
                return

        """generate nex population"""
        population = generateNextPopulation(population, fitness)
        generation += 1

""" default size is 8 cus 8-queens:)"""
size = 8
final(size)
