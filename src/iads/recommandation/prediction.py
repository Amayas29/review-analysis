from surprise.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def model_pred(model, user_item):
    user = user_item["author"]
    game = user_item["title_id_jeu"]
    prediction = model.predict(user, game)

    return prediction.est


def gs_pred(data, model, param_grid):
    gs = GridSearchCV(model, param_grid, measures=['rmse'], cv=5)
    gs.fit(data)

    model = gs.best_estimator["rmse"]
    model.fit(data.build_full_trainset())

    print(gs.best_params["rmse"])

    plt.plot(gs.cv_results["mean_test_rmse"])
    params = gs.cv_results["params"]
    plt.xticks(np.arange(len(params)), params, rotation=90)
    plt.show()

    return model

def get_cosine_matrix(df,col):

    if col in ["description","categories"] :
        tfidf = TfidfVectorizer()
        matrix = tfidf.fit_transform(df[[col]].apply(lambda x: ' '.join(x), axis=1))

    elif col in [['enfant', 'ado', 'adulte'],['solo', 'duo', 'multi']] :
        matrix = np.vstack([row.to_numpy().ravel() for _, row in df[col].iterrows()])
        
    else :
        df_concat = pd.DataFrame({'concat': df[col].apply(lambda x: ' '.join(x), axis=1)})
        tfidf = TfidfVectorizer()
        matrix = tfidf.fit_transform(df_concat.apply(lambda x: ' '.join(x), axis=1))


    similarity_matrix = cosine_similarity(matrix)
    np.fill_diagonal(similarity_matrix, 1) #Pour les catégories

    return similarity_matrix
