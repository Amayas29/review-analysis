# Avancement PLDAC

## Semaine 1 (6/02) -- Prétraitement des données

Avancement :
- One hot encoding sur le casting (créateur, illustrateur, editeur, distributeur)
- Séparer le game-play en 3 colonnes : nb joueurs, âge, temps de jeu
- One hot encoding sur l'âge (enfant, ado, adulte)
- Suppression des url
- Modifier la date de publication des avis de sorte à ne garder que l'année

Problèmes rencontrés :
- Un même jeu peut avoir plusieurs identifiants
- Certains jeux ont le même nom

Solutions trouvées :
- Supprimer les duplicatas en veillant à ne pas supprimer des jeux différents (idem sur la base d'avis)
- Récupérer le nom dans l'url pour différencier toutes les versions d'un même jeu et qu'ainsi tous les jeux soient uniques. Ce qui amène à changer le titre dans la base de données des avis

Remarques :
- Beaucoup de notes à 0, pourquoi?

**Réunion** :
- Scrapper le prix? Pas sûr que cela vaille le coup
- Estimation de densité pour représenter les notes
- Commencer à entraîner un petit classifieur, regarder les features qui ont le plus de poids dans la classification
- Traiter les utilisateurs

## Semaine 2 (13/02) -- Suite prétraitement des données et statistiques
Avancement :
- Statistiques sur les avis et les jeux (cf. stats_avis et stats_jeux)
- Wordcloud des avis e

Problèmes rencontrés :
- Beaucoup de jeux avec une note nulle (35%)

Solutions trouvées :
- Les jeux avec une note nulle sont en fait des jeux qui n'ont pas d'avis. 

Remarques :
- Le comportement des 10 premiers utilisateurs (en nb d'avis) est très différent
- Très peu de données sur le distributeur : à supprimer
- Certains jeux n'ont pas de catégorie
- Les "Notes" et la "Notes rectifiées" sont très corrélées, on décide donc de ne garder que l'attribut "Note"
- La note Finkel est une combinaison linéaire entre la note et le nombre d'avis d'un jeu

**Réunion** :
- (Conseils pour l'autre groupe mais intéressants : possibilité d'abandonner des reviews positives pour gérer l'équilibre des classes, sinon médiane à 8 + normalisation des notes de -1 à 1 pour la régression linéaire + faire varier le vocab pour voir les différentes performances + F1 score plus adapté aux classes déséquilibrées que l'accuracy + utiliser Kmeans dans un espace plus faible, avec un dictionnaire plus restreint, pas adapté ici)
- Ajouter une catégorie "duo" plutôt que juste "solo" et "multijoueurs"
- Durée de jeu : enlever estimation de densité
- Clusterisation des catégories de jeux à partir des tags sur les catégories (= réduction de la dimension sur le nombre de tags)
- Apprendre un classifieur qui prédit le cluster mais à partir de texte (soit la description du jeu, soit les avis du jeu)


## Semaine 3 (20/02) -- Clustering et prédiction
Avancement :
- Clustering catégories : kmeans (fusionne certaines catégories)
- Test de deux mesures (importance et fréquence) : la fréquence donne de meilleurs résultats, on l'utilise pour ne garder qu'une seule catégorie pour les jeux qui en ont plusieurs
- Supprimer catégories qui apparaissent moins de 6 fois
- Supprimer les descriptions avec un nombre de caractères inférieur à un certain seuil

Problèmes rencontrés :
- Certaines descriptions en anglais
- D'autres ont "Aucune description"
- La détection de langue trouve une dizaine de langues différentes (sachant que la plupart sont mal classés à cause d'une description trop courte) et la traduction est impossible

Solutions trouvées :
- Détecter la langue des descriptions
- Remplacer "Aucune description" par un NaN
- Se débarrasser des descriptions écrites dans une langue étrangère

Remarques :
- Certains jeux n'ont ni catégorie ni description (env 200), on les supprimera


