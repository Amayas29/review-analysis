import numpy as np

def delete_dup(df):
    # Regrouper les lignes par auteur et titre et trouver l'indice de la date la plus récente
    idx = df.groupby(['author', 'title'])['date_published'].idxmax()
    # Sélectionner les lignes uniques à partir de ces indices
    unique_rows = df.loc[idx]
    return unique_rows

def clean_user(df,nb_avis_min=5):
    users, count_users = np.unique(df["author"],return_counts=True)
    users_filtred = users[count_users >= nb_avis_min]
    u=len(users)-len(users_filtred)
    index_df_filter = np.isin(df["author"], users_filtred)

    return u,df[index_df_filter][['author', 'title', 'note']]

def clean_game(df,nb_avis_min=5):
    game, count_game = np.unique(df["title"],return_counts=True)
    game_filtred = game[count_game >= nb_avis_min]
    g=len(game)-len(game_filtred)
    index_df_filter = np.isin(df["title"], game_filtred)
    return g,df[index_df_filter][['author', 'title', 'note']]