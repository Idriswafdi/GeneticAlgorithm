import random

from deap import base
from deap import creator
from deap import tools
from statistics import mean
from math import sin

creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
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
N_Screen = 4

# Structure initializers
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.prix, toolbox.jour, toolbox.weekend, toolbox.mois,
                  toolbox.horaire, toolbox.audience, toolbox.alloue), n=N_Screen)

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

def GenAlg(CrossoverP, MutationP, PenAdapt, population_size, budget_size):
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

# ----------------------------------------------------PREMIERE EVAL---------------------------------------------
    def feasible(individual):
        """Feasibility function for the individual. Returns True if feasible False
    otherwise."""
        if sum(individual[0::7]) < budget_size :
            return True
        return False

    def evalFct(individual, adaptiveP):
        """Evaluation function for the individual."""
        prixInd = individual[0::7]
        audienceInd = individual[5::7]

        if feasible(individual):
            return sum(prixInd), mean(audienceInd)
        else:

            return sum(prixInd) - adaptiveP, mean(audienceInd) - adaptiveP/1000

    toolbox.register("evaluate", evalFct, adaptiveP=PenAdapt)

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

# ----------------------------------------------------DEBUT EVOLUTION---------------------------------------------
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

# ----------------------------------------------------CROSSOVER----------------------------------------------------
        for child1, child2 in zip(offspring[::2], offspring[1::2]):


            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                print("before crossover %s, %s: " % (child1, child2))
                toolbox.mate(child1, child2)
                print("new crossover %s, %s: " % (child1, child2))

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values
# ----------------------------------------------------MUTATION----------------------------------------------------
        for mutant in offspring:
            alloc = mutant[6::7]
            # mutate an individual with probability MUTPB
            for y in range(len(alloc)):
                if random.random() < MUTPB:
                    #print("mutation a eu lieu ! avant: %s" % mutant[6::7])
                    if alloc[y] == 1:
                        #print("avant c'etait un %s" % alloc[y])
                        alloc[y] = 0
                        #print("maintenant c'est un %s" % alloc[y])
                    else:
                        #print("avant c'etait un %s" % alloc[y])
                        alloc[y] = 1
                        #print("maintenant c'est un %s" % alloc[y])
                    mutant[6::7] = alloc
                    #print("mutation a eu lieu ! apres: %s" % mutant[6::7])
                    del mutant.fitness.values
# ----------------------------------------------------RECALCUL FITNESS---------------------------------------------
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring
        best_ind = tools.selBest(pop, 1)[0]
        print("Best individual has %s, %s" % (sum(best_ind[0::7]), mean(best_ind[5::7])))

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        BestOne = tools.selBest(pop, 5)
        #print("  Best 3 solutions %s" % BestOne)
# --------------------------------------------------------FEEDBACK---------------------------------------------------
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

# ----------------------------------------------------MODIF PENALITE---------------------------------------------------

        # fitness function avec pénalité adaptative
        def adaptiveEval(individual, adaptiveP):
            prixInd = individual[0::7]
            audienceInd = individual[5::7]

            if feasible(individual):
                return sum(prixInd), mean(audienceInd)
            else:

                return sum(prixInd) - adaptiveP, mean(audienceInd) - adaptiveP / 1000

        toolbox.register("evaluate", adaptiveEval, adaptiveP=PenAdapt)




    print("-- End of evolution --")


    best_ind = tools.selBest(pop, 1)[0]
    worst_ind = tools.selWorst(pop, 1)[0]
    print(" Pénalité augmentée %s fois" % comptAug)
    print(" Pénalité diminuée %s fois" % comptDim)
    print(" Pénalité non changée %s fois" % comptDiv)
    print(" Pénalité %s" % PenAdapt)
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    print("Best individual has %s, %s" % (sum(best_ind[0::7]), mean(best_ind[5::7])))
    #print("Worst individual is %s, %s" % (worst_ind, worst_ind.fitness.values))



if __name__ == "__main__":
    # CrossoverP, MutationP, PenAdapt, population_size, budget_size
    GenAlg(0.5, 0.1, 100, 10, 2000)
