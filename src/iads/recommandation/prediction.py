from surprise.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, pairwise_kernels

from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import networkx as nx
import matplotlib.pyplot as plt


def model_pred(model, user, game=None):
    if game is None:
        user_ = user["author"]
        game = user["title"]
        user = user_

    prediction = model.predict(user, game)
    return prediction.est


def mrr(user_jeux_preference):
    def rr(list_jeux_preference):
        relevant_indexes = np.asarray(list_jeux_preference).nonzero()[0]

        if len(relevant_indexes) > 0:
            return 1 / (relevant_indexes[0] + 1)

        return 0

    return np.mean([rr(l) for l in user_jeux_preference])


def ndcg_at_k(user_jeux_preference, k=10):
    ndcg_list = []

    for l in user_jeux_preference:
        relevant_indexes = np.asarray(l).nonzero()[0]

        if len(relevant_indexes) == 0:
            ndcg_list.append(0)
            continue

        idcg = 0
        for i in range(min(k, len(relevant_indexes))):
            idcg += 1 / np.log2(i + 2)

        dcg = 0
        for i in np.argsort(l)[::-1][:k]:
            if i in relevant_indexes:
                dcg += 1 / np.log2(np.where(relevant_indexes == i)[0][0] + 2)

        ndcg = dcg / idcg
        ndcg_list.append(ndcg)

    return np.mean(ndcg_list)


def get_user_predictions(model, data):
    ground_truth = data["ground_truth"]
    already_play = data["already_play"]
    existing_games = data["existing_games"]

    user_jeux_preference = []

    for user, will_play in tqdm(ground_truth.items()):
        if user not in already_play:
            continue

        l = []
        will_play = set(will_play)
        has_play = set(already_play[user])
        can_play = [
            (game, model_pred(model, user, game)) for game in existing_games - has_play
        ]

        for game, score in reversed(sorted(can_play, key=lambda x: x[1])):
            if game not in will_play:
                l.append(0)
                continue

            l.append(1)
            break

        l[-1] = 1
        user_jeux_preference.append(l)

    return user_jeux_preference


def gs_pred(dict_data, model, param_grid, plot=True):
    gs = GridSearchCV(model, param_grid, measures=["rmse"], cv=5)
    gs.fit(dict_data["data"])

    model = gs.best_estimator["rmse"]
    model.fit(dict_data["data"].build_full_trainset())

    print(gs.best_params["rmse"])

    if plot:
        plt.figure(figsize=(10, 10))
        plt.plot(gs.cv_results["mean_test_rmse"])
        params = gs.cv_results["params"]
        plt.xticks(np.arange(len(params)), params, rotation=90)
        plt.ylim(min(gs.cv_results["mean_test_rmse"]) - 1, max(gs.cv_results["mean_test_rmse"]) + 1)
        plt.show()

    predictions = get_user_predictions(model, dict_data)
    gs_mrr = mrr(predictions)
    print(f"MRR : {gs_mrr}")
    print(f"Rang du jeu : {1/gs_mrr}")

    return model


def get_cosine_matrix(df, col):
    if col in ["description", "categories"]:
        tfidf = TfidfVectorizer()
        matrix = tfidf.fit_transform(df[col].values)

    elif col in [["enfant", "ado", "adulte"], ["solo", "duo", "multi"]]:
        matrix = df[col].to_numpy()

    else:
        matrix = TfidfVectorizer().fit_transform(
            df[col].apply(lambda x: " ".join(x), axis=1).values)

    similarity_matrix = cosine_similarity(matrix)
    np.fill_diagonal(similarity_matrix, 1)

    return similarity_matrix


def get_kernel_matrix(df, col, kernel):
    if col in ["description", "categories"]:
        tfidf = TfidfVectorizer()
        matrix = tfidf.fit_transform(df[col].values)

    elif col in [["enfant", "ado", "adulte"], ["solo", "duo", "multi"]]:
        matrix = df[col].to_numpy()

    else:
        matrix = TfidfVectorizer().fit_transform(
            df[col].apply(lambda x: " ".join(x), axis=1).values)

    similarity_matrix = pairwise_kernels(matrix, metric=kernel)
    np.fill_diagonal(similarity_matrix, 1)

    return similarity_matrix


def graphe_knn(matrix, k=5):
    G = nx.Graph()

    for i in tqdm(range(matrix.shape[0])):
        neighbors = matrix[i].argsort()[-k-1:-1][::-1]

        for neighbor in neighbors:
            weight = matrix[i][neighbor]
            G.add_edge(i, neighbor, weight=weight)

    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=50)
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.axis('off')
    plt.show()
