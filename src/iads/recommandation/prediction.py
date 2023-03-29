from surprise.model_selection import GridSearchCV
from tqdm import tqdm
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
