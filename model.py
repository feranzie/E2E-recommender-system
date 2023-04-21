import os
import json
import base64

import boto3
import mlflow

def get_model_location(run_id):
    model_location = os.getenv("MODEL_LOCATION")

    if model_location is not None:
        return model_location

    model_bucket = os.getenv("MODEL_BUCKET", "mlflow-model-feranmi")
    experiment_id = os.getenv("MLFLOW_EXPERIMENT_ID", "2")
    
    model_location = f"s3://{model_bucket}/{experiment_id}/{run_id}/artifacts/model"
    return model_location

def load_model(run_id):
    model_path = get_model_location(run_id)
    model = mlflow.pyfunc.load_model(model_path)
    return model

def base64_decode(encoded_data):
    decoded_data = base64.b64decode(encoded_data).decode("utf-8")
    ride_event = json.loads(decoded_data)
    return ride_event

class ModelService:
    def __init__(self, model, model_version=None, callbacks=None):
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []

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
        return recomendation[:10]