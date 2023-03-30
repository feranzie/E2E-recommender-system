
import mlflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")
RUN_ID='fa350b60cf564ff1a1d3341e2ac38cbe'
#logged_model = f'mlflow-artifacts:/728115650857226939/eb5ec70b031246f3a1336ba5ea0afe76/artifacts/model'
logged_model=f'mlflow-artifacts:/773732190913986377/{RUN_ID}/artifacts/model'
#logged_model = f'runs:/{RUN_ID}/model'
model = mlflow.sklearn.load_model(logged_model)
import pandas as pd
#IMPORTING DATA FROM CSV FILES INTO A DATAFRAME FOR ANALYSIS 
post = pd.read_csv("data/posts.csv")
user = pd.read_csv("data/users.csv")
view = pd.read_csv("data/views.csv")
post["category"] = post["category"].fillna("random")
cat = {}
for i in post["category"]:
    cat.update({i:[]})
    for j in i.split("|"):
        cat[i].append(j)
print(cat)
updated_data =  []
for i in cat:
    dummy = post[post['category']==i]
    id = dummy['_id'].values[0]
    title = dummy['title'].values[0]
    post_type = dummy[' post_type'].values[0]
    for j in cat[i]: 
        dict1 = {}
        dict1.update({'_id':id})
        dict1.update({'title':title})
        dict1.update({'category':j})
        dict1.update({' post_type':post_type})
        updated_data.append(dict1)
post1 = pd.DataFrame(updated_data)
post1.rename(columns={"_id":'post_id'}, inplace = True)
user.rename(columns={"user_id":'post_id'},  inplace = True)
main = pd.merge(view,post1)
users = list(main["user_id"].unique())
categories = list(main["category"].unique())

#MATRIX WILL BE OF 88,235
user_mat = [[] for i in range(len(users))]
for i in range(len(users)):
    for j in range(len(categories)):
        value = len(main[(main["user_id"]==users[i]) & (main["category"]==categories[j])])
        user_mat[i].append(value)
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