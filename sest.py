import pandas as pd
import pickle
import scipy.sparse as sp


def recommender(user_id):
    with open('users.pkl', 'rb') as f:
        users = pickle.load(f)
    main=pd.read_csv('main.csv')
    matrix = sp.load_npz('matrix.npz')
    with open('model.bin', 'rb') as f_in:
        model = pickle.load(f_in)
    data=matrix
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

print(recommender('5df49b32cc709107827fb3c7')[:10])