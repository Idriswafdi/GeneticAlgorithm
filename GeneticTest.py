import random

from deap import base
from deap import creator
from deap import tools
from math import sin

creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("prix", random.randint, 100, 1500)
toolbox.register("jour", random.randint, 1, 30)
toolbox.register("weekend", random.randint, 0, 1)
toolbox.register("mois", random.randint, 1, 12)
toolbox.register("horaire", random.randint, 0, 23)
toolbox.register("audience", random.uniform, 1.00, 5.00)
toolbox.register("alloue", random.randint, 0, 1)

# Nombres d'ecrans dans un individu
N_Screen = 10

# Structure initializers
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.prix, toolbox.jour, toolbox.weekend, toolbox.mois, toolbox.horaire, toolbox.audience, toolbox.alloue), n=N_Screen)

# define the population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# ----------
# Operator registration
# ----------
# register the crossover operator
toolbox.register("mate", tools.cxOnePoint)

# operator for selecting individuals for breeding the next
# generation: each individual of the current generation
# is replaced by the 'fittest' (best) of three individuals
# drawn randomly from the current generation.
toolbox.register("select", tools.selTournament, tournsize=3)


# ----------

def GenAlg(CrossoverP, MutationP, PenAdapt, population_size):
    random.seed(64)

    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=population_size)


    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB = CrossoverP
    MUTPB = MutationP

    def feasible(individual):
        """Feasibility function for the individual. Returns True if feasible False
    otherwise."""

        if -3 < individual[0] < 9 and individual[1] > 0 and individual[2] != 0:
            return True
        return False

    def evalFct(individual, adaptiveP):
        """Evaluation function for the individual."""
        prix = individual[0]
        audience = individual[5]

        if feasible(individual):
            return (x1 - 25) ** 2 * sin(x2) * (x3 / 3),
        else:

            return ((x1 - 25) ** 2 * sin(x2) * (x3 / 3)) / adaptiveP,

    toolbox.register("evaluate", evalFct, adaptiveP = PenAdapt)

    print("Start of evolution")

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        #print(ind.fitness.values)



    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0
    comptDim = 0
    comptAug = 0
    comptDiv = 0

    # Begin the evolution
    while g < 100:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)
        #print(pop)
        i = 0
        for inf in pop:
            if feasible(inf) is False:
                #print(inf)
                i = i+1
        print("  incompatibles: %s" % i)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                print("mutation a eu lieu ! avant: %s" % mutant[6])
                if mutant[6] == 1:
                    mutant[6] = 0
                    print("mutation a eu lieu ! apres: %s" % mutant[6])
                else:
                    mutant[6] = 1
                    print("mutation a eu lieu ! apres: %s" % mutant[6])

                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        #sum2 = sum(x * x for x in fits)
        #std = abs(sum2 / length - mean ** 2) ** 0.5

        i = 0

        BestOne = tools.selBest(pop, 5)
        print("  Best 3 solutions %s" % BestOne)

        # si les 3 best sont faisables
        if all(feasible(i) for i in BestOne):
            PenAdapt = PenAdapt/2
            print(" Pénalité diminuée ! %s" % PenAdapt)
            comptDim = comptDim + 1

        # si les 3 best sont infaisables
        elif not any(feasible(i) for i in BestOne):
            PenAdapt = PenAdapt * 2
            print(" Pénalité augmentée! %s" % PenAdapt)
            comptAug = comptAug + 1

        # si il y a de la diversité
        else:
            print(" Aucun changement de pénalité ! %s" % PenAdapt)
            comptDiv = comptDiv + 1



        # fitness function avec pénalité adaptative
        def adaptiveEval(individual, adaptiveP):
            x1 = individual[0]
            x2 = individual[1]
            x3 = individual[2]

            if feasible(individual):
                return (x1 - 25) ** 2 * sin(x2) * (x3 / 3),
            else:
                #
                return ((x1 - 25) ** 2 * sin(x2) * (x3 / 3)) / adaptiveP,

        toolbox.register("evaluate", adaptiveEval, adaptiveP = PenAdapt)




    print("-- End of evolution --")


    best_ind = tools.selBest(pop, 1)[0]
    worst_ind = tools.selWorst(pop, 1)[0]
    print(" Pénalité augmentée %s fois" % comptAug)
    print(" Pénalité diminuée %s fois" % comptDim)
    print(" Pénalité non changée %s fois" % comptDiv)
    print(" Pénalité %s" % PenAdapt)
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    print("Worst individual is %s, %s" % (worst_ind, worst_ind.fitness.values))



if __name__ == "__main__":
    GenAlg(0.5, 0.1, 9, 10)