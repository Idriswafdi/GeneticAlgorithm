# GeneticAlgorithm
Code de l'algorithme génétique dans le fichier Genetictest.py

# Explication du code:

- Initialisation de la population et d'un individu (on crée les mots-clés "population", "individual", "mate", "select")

- "PREMIERE EVAL" Première evaluation de la population, avec la pénalité standard

- "DEBUT EVOLUTION" Boucle des générations

- "CROSSOVER" et "MUTATION" les deux opérateurs classiques, on utilise un croisement à un point et une mutation aléatoire. La mutation affecte uniquement le bit d'allocation (gène "allouer")
  
- "RECALCUL FITNESS" on recalcule l'evaluation de la population, avec la pénalité modifié en fonction de les meilleurs 3 individus de la dernière génération

- "FEEDBACK" on recupère les 3 derniers meilleurs individus de la dernière génération, ce qui nous permet de modifier la pénalité

- "MODIF PENALITE" on met à jour la fonction d'évaluation avec la nouvelle pénalité 

# Paramétres à rentrer

L'algoritme prend comme paramétres: 

- la probabilité que le croisement ait lieu

- la probabilité que la mutation ait lieu

- la pénalité adaptative à appliquer 

- la taille de la population

- le budget du client (contrainte)
