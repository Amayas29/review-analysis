# Avancement PLDAC

## Semaine 1 (6/02) -- Prétraitement des données

Avancement :
- Extractions des informations du casting (créateur, illustrateur, editeur, distributeur)
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
- Wordcloud des avis

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
- Ajouter une catégorie "duo" plutôt que juste "solo" et "multijoueurs"
- Durée de jeu : enlever estimation de densité
- Clusterisation des catégories de jeux à partir des tags sur les catégories (= réduction de la dimension sur le nombre de tags)
- Apprendre un classifieur qui prédit le cluster mais à partir de texte (soit la description du jeu, soit les avis du jeu)


## Semaine 3 (20/02) -- Clustering et prédiction
Avancement :
- Clustering syntaxique des catégories : kmeans (fusionne certaines catégories)
- Test de deux mesures (importance et fréquence) : la fréquence donne de meilleurs résultats, on l'utilise pour ne garder qu'une seule catégorie pour les jeux qui en ont plusieurs
- Supprimer les catégories qui apparaissent moins de 6 fois
- Supprimer les descriptions de langue etrangeres avec un nombre de mots superieur à un certain seuil
- Nettoyage des descriptions (stopwords, ponctuation, lemmatization ...)
- Prédiction de la catégorie à partir de la description (en utilisant Naive bayes, SVM et Random Forest)

Problèmes rencontrés :
- Certaines descriptions en anglais
- D'autres ont "Aucune description"
- La détection de langue trouve une dizaine de langues différentes (sachant que la plupart sont mal classés à cause d'une description trop courte) et la traduction est impossible

Solutions trouvées :
- Détecter la langue des descriptions
- Remplacer "Aucune description" par un NaN
- Se débarrasser des longues descriptions écrites dans une langue étrangère

Remarques :
- Certains jeux n'ont ni catégorie ni description (env 200)

**Réunion** :
- Utiliser CountVectorizer plutôt que Tfidf sur les descriptions
- Pour les catégories, ne pas sélectionner qu'une seule par jeu car perte d'information. Faire du multilabel (one vs all puis ranking label)
- Oublier la génération de catégorie
- Jouer sur les paramètres de la prédiction (SVM -> pénalisation, Random Forest -> nombre d'arbres et profondeur)
- Conserver les mots peu fréquents pour la classification/prédiction, peut aussi apporter des infos
- Pour tester plusieurs pipelines et modèles : stocker les différentes pipelines sur disque, créer une fonction qui permet de changer les paramètres et les appliquer aux modèles avec différents paramètres
- Faire un test déséquilibré avec la vraie distribution des données afin d'être en accord avec la réalité
- A faire : recommandation (compléter notebook et lire document)
- Content based : proche des k-nn, regarde le contenu des items
- Filtrage collaboratif : approche bigraphe, regarde les appréciations des items
- Ou système hybride

## Semaine 4 (20/03) -- Découverte systèmes de recommandation
Avancement :
- Création matrice item-user

Remarque : 
- Principe collaborative filtering : apprendre des profils d'utilisateurs et d'items puis prédire une note. Le but étant de recommander les items correspondant aux meilleures notes par la suite

**Réunion** :
- Comparer content-based et filtrage collaboratif
- Garder uniquement quelques utilisateurs (15-20, qui ont le plus noté) et les jeux qui ont le plus d'avis
- Tester les algos "surprise" du notebook
- Problème si on veut conserver les 5 items qui ont reçu la meilleure prédiction de note : on risque de prédire toujours la même chose. Solution : prédire 3 items de la même cat, 1 d'une cat proche et 1 d'un cat très éloignée par ex
- Utiliser algo BPR (Bayesian Personalized Ranking) : donne un score entre 0 et 1 si la personne risque d'apprécier l'item ou non. Utile car la préférence ne s'exprime pas qu'à traver les notes mais aussi à travers ce qu'ils notes (un certain type de jeu par ex)
- Comparer avec les algos de factorisation matricielle : prédit notes évaluées au sens des moindres carrés
- Pour comparer, sortir les items prédits des deux méthodes et les comparer (nous dira seulement à quel point les algos font la même chose ou non)
- Réutiliser le boulot qui a été fait sur les catégories
- Etudier les variantes de la factorisation matricielle
- Attention : risque de prédire uniquement une note (5) et risque de sur-apprentissage car matrices très sparses donc + de param que de notes à prédire.
- Solution : réduire taille matrice et régulariser (reconstruire les notes en minimisant l'erreur au sens des MSE et en minimisant la norme des matrices)
- On pourrait aussi ajouter des colonnes et apprendre un profil pour des cat de jeux


## Semaine 5 (27/03) -- Prise en main filtrage collaboratif
Avancement :
- Distribution des notes
- Tri des jeux avec un nb d'avis < à 5
- Test sur différents algorithmes :
- - Baseline
- - SVD & SVD ++ (GridSearch sur le nb de facteurs)
- - KNN (GridSearch sur k)
- - SlopeOne
- Meilleur algo en fonction de MSE
- Test reco avec les différents algos

**Réunion** :
- Vérifier que lorsqu'on sépare des jeux en différentes versions il s'agisse bien d'extensions et non simplement d'une autre référence. Si autre référence (donc 2 jeux identiques), merger les deux et récupérer la dernière note de l'utilisateur s'il a noté les deux ou faire une moyenne
- Pour réduire le nb de jeux et utilisateurs : procéder par itérations sur les jeux et les utilisateurs (en veillant à ne pas se retrouver avec une base trop pauvre)
- n factors trop grand pour SVD, aller de 10 à 50 pour éviter sur-apprentissage (peut être + grand si on touche la reg)
- Changer paramètres de régularisation pour SVD (si lr diminue, nb epoch augmente)
- Trop sparse pour KNN, passer par cosine ?
- Les métriques MSE et RMSE sont pas ouf pcq dans notre cas il suffirait de prédire une note entre 8 et 10 pour minimiser le cout, donc essayer MRR, MAP et MDCG (prend plus en compte le rang et pénalise plus les erreurs)
- Faire de la visualisation et interprétation : t-sne des représentations latentes (des jeux)
- Similarité de contenu (content-based sur cat et descr avec cosine, utiliser graphe knn)

## Semaine 6 (03/04) -- Suite filtrage collaboratif et content based
Avancement :

**Réunion** : 
- Baseline : faire varier encore + la reg
- Se poser la question : est ce qu'on bat l'algo naïf qui sort toujours la moyenne?
- Vérifier qu'on est pas juste en train de prédire les items les + populaires
- Augmenter reg_u et reg_i en fonction du nombre d'avis moyen par jeu
- Mettre la perf train/test pour voir sur/sous apprentissage
- Heatmap correlation user/item pour filtrage co pour param optimaux
- Imshow à la place des courbes
- Revoir le knn, pas normal qu'il soit aussi mauvais
- T-SNE de sklearn (scatter plot) avec couleur des points en fonction de la catégorie (sûrement mieux qu'avec tensorflow)
- Prendre du recul pour "vendre" le système
- Démarrage à froid, pour faire des premières recommandations en justifiant
- Co-clustering pour matrices de similarité
- Laisser tomber tous les autres poids sauf description? Utiliser des clusters de catégories
- Plus proches voisins pour l'analyse quantitative pour content-based (avec les notes par ex)