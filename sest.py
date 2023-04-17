import pandas as pd
import pickle
import scipy.sparse as sp
def prepare():
    with open('users.pkl', 'rb') as f:
        users = pickle.load(f)
    main=pd.read_csv('main.csv')
    matrix = sp.load_npz('matrix.npz')
    return main, matrix, users
#users=data_helper.users

def recommender(user_id, data=matrix, model=model):
    model.fit(data)
    index = users.index(user_id)
    current_user = main[main['user_id']==user_id]
    distances, indices = model.kneighbors(data[index], 15)
    recomendation = []
    for i in indices[0]:
        user = main[main['user_id']==users[i]]
        for i in user['category'].unique():
            if i not in current_user['category'].unique():
                recomendation.append(i)
    return recomendation