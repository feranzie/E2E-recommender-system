#IMPORTING LIBRARIES
import numpy as np
import pandas as pd
import mlflow
from prefect import flow, task, get_run_logger



@task
def read_data(path):
    post = pd.read_csv(f"{path}/posts.csv")
    user = pd.read_csv(f"{path}/users.csv")
    view = pd.read_csv(f"{path}/views.csv")
    user.rename(columns={"user_id":'post_id'}, inplace = True)

    return post, user, view


@task
def prepare_features(post, user, view):
    logger = get_run_logger()
    post["category"] = post["category"].fillna("random")
    cat = {}
    for i in post["category"]:
        cat.update({i:[]})
    for j in i.split("|"):
        cat[i].append(j)
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
    user.rename(columns={"user_id":'post_id'}, inplace = True)
    post1.rename(columns={"_id":'post_id'}, inplace = True)
    main = pd.merge(view,post1, left_index=True, right_index=True)
    users = list(main["user_id"].unique())
    categories = list(main["category"].unique())

    user_mat = [[] for i in range(len(users))]
    for i in range(len(users)):
        for j in range(len(categories)):
            value = len(main[(main["user_id"]==users[i]) & (main["category"]==categories[j])])
            user_mat[i].append(value)
    from scipy.sparse import csr_matrix 
    user_mat = csr_matrix(user_mat)
    logger.info("Successful!y prepared data")
    return user_mat
@task
def train_model(user_mat):
    logger = get_run_logger()
    from sklearn.neighbors import NearestNeighbors
    model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=15)
    model.fit(user_mat)
    with mlflow.start_run(run_name="rec system"):
        mlflow.sklearn.log_model(model, "model")
    logger.info("model trained Successful!y ")
    return model

@flow
def main_flow(path: str = 'data'):
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("recommender")

    # Load
    post,user,view=read_data(path)
    print('read data')
    #prepare data
    user_mat=prepare_features(post, user, view)
    print('prepared features')

    #training
    train_model(user_mat)
    print('train')

main_flow()   
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import IntervalSchedule
from datetime import timedelta

Deployment.build_from_flow(
    flow=main_flow,
    name="model_training",
    # schedule=IntervalSchedule(interval=timedelta(weeks=1)),
    work_queue_name="ml",
)