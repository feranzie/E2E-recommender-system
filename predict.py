
import mlflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")
RUN_ID='fa350b60cf564ff1a1d3341e2ac38cbe'
#logged_model = f'mlflow-artifacts:/728115650857226939/eb5ec70b031246f3a1336ba5ea0afe76/artifacts/model'
logged_model=f'mlflow-artifacts:/773732190913986377/{RUN_ID}/artifacts/model'
#logged_model = f'runs:/{RUN_ID}/model'
model = mlflow.sklearn.load_model(logged_model)

def recommender(user_id, data=user_mat, model=model):
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
#     print(indices)
print(recommender('5df49b32cc709107827fb3c7')[:10])