import os
import json
import boto3
import base64

import mlflow
import pandas as pd
import pickle
import scipy.sparse as sp
#os.environ["AWS_PROFILE"] = "feranmi" 
kinesis_client = boto3.client('kinesis')

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'recommender-system')

RUN_ID='fa350b60cf564ff1a1d3341e2ac38cbe'
#logged_model = f'mlflow-artifacts:/728115650857226939/eb5ec70b031246f3a1336ba5ea0afe76/artifacts/model'
logged_model=f'mlflow-artifacts:/773732190913986377/{RUN_ID}/artifacts/model'
#logged_model = f'runs:/{RUN_ID}/model'
model = mlflow.sklearn.load_model(logged_model)



with open('users.pkl', 'rb') as f:
    users = pickle.load(f)
main=pd.read_csv('main.csv')
matrix = sp.load_npz('matrix.npz')


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
#     print(indices)
#print(recommender('5df49b32cc709107827fb3c7')[:10])
#recommender(users[0])[:10]


def lambda_handler(event, context):

    predictions_events = []

    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        ride_event = json.loads(decoded_data)

    
        # print(ride_event)
        ride = ride_event['ride']
        ride_id = ride_event['ride_id']
    
        features = prepare_features(ride)
        prediction = predict(features)
    
        prediction_event = {
            'model': 'ride_duration_prediction_model',
            'version': '123',
            'prediction': {
                'ride_duration': prediction,
                'ride_id': ride_id   
            }
        }

        predictions_events.append(prediction_event)


    return {
        'predictions': predictions_events
    } 