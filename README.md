# GeneticAlgorithm
Code de l'algorithme génétique dans le fichier GeneticTest.py

# Explication du code:

- Initialisation de la population et d'un individu (on crée les mots-clés "population", "individual", "mate", "select")

- "PREMIERE EVAL" Première evaluation de la population, avec la pénalité standard

- "DEBUT EVOLUTION" Boucle des générations

- "CROSSOVER" et "MUTATION" les deux opérateurs classiques, on utilise un croisement à un point et une mutation aléatoire. La mutation affecte uniquement le bit d'allocation (gène "allouer")
  
- "RECALCUL FITNESS" on recalcule l'evaluation de la population, avec la pénalité modifié en fonction de les meilleurs 3 individus de la dernière génération

- "FEEDBACK" on recupère les 3 derniers meilleurs individus de la dernière génération, ce qui nous permet de modifier la pénalité

- "MODIF PENALITE" on met à jour la fonction d'évaluation avec la nouvelle pénalité 

# Composition d'un individu

— Prix(compris entre 100€ et 1500€) : Donnée indiquant le prix
—Jour(compris entre 1 et 30) : Jour du mois, donnée normalisée
—Weekend(Booléen) : Donnée qui nous indique si on est en week-end
—Mois(compris entre 1 et 12) : Donnée indiquant le mois
—Horaire(compris entre 0 et 23) : Donnée indiquant l’horaire de la journée
—Audience(compris entre 1.00 et 5.00) : Donnée indiquant l’indice d’audience
—Alloué(Booléen) : Donnée qui nous indique si le créneaux sera alloué ou pas,donnée initialement à 0.

# Paramétres à rentrer

L'algoritme prend comme paramétres: 

- la probabilité que le croisement ait lieu

- la probabilité que la mutation ait lieu

- la pénalité adaptative à appliquer 

- la taille de la population

- le budget du client (contrainte)
