import json
import os
import pickle
import datetime
import pandas
import pyarrow.parquet as pq
from evidently import ColumnMapping
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab, RegressionPerformanceTab
from evidently.model_profile import Profile
from evidently.model_profile.sections import (
    DataDriftProfileSection, RegressionPerformanceProfileSection)
from prefect import flow, task
from pymongo import MongoClient

MONGO_CLIENT_ADDRESS = "mongodb://localhost:27017/"
MONGO_DATABASE = "prediction_service"
PREDICTION_COLLECTION = "data"
REPORT_COLLECTION = "report"
REFERENCE_DATA_FILE = "../datasets/green_tripdata_2021-03.parquet" # Modify this for Q7
TARGET_DATA_FILE = "target.csv"
MODEL_FILE = os.getenv('MODEL_FILE', '../web-service/model.bin') # Modify this for Q7

@task
def upload_target(filename):
    client = MongoClient(MONGO_CLIENT_ADDRESS)
    collection = client.get_database(MONGO_DATABASE).get_collection(PREDICTION_COLLECTION)
    with open(filename) as f_target:
        for line in f_target.readlines():
            row = line.split(",")
            collection.update_one({"id": row[0]},
                                  {"$set": {"target": float(row[1])}}
                                 )
@task
def load_reference_data(filename):
    
    with open(MODEL_FILE, 'rb') as f_in:
        model = pickle.load(f_in)
    
    return reference_data

@task
def fetch_data():
    client = MongoClient(MONGO_CLIENT_ADDRESS)
    data = client.get_database(MONGO_DATABASE).get_collection(PREDICTION_COLLECTION).find()
    df = pandas.DataFrame(list(data))
    return df

@task
def run_evidently(ref_data, data):

    ref_data.drop(['ehail_fee'], axis=1, inplace=True)
    data.drop('ehail_fee', axis=1, inplace=True)  # drop empty column (until Evidently will work with it properly)

    profile = Profile(sections=[DataDriftProfileSection(), RegressionPerformanceProfileSection()])
    mapping = ColumnMapping(prediction="prediction", numerical_features=['trip_distance'],
                            categorical_features=['PULocationID', 'DOLocationID'],
                            datetime_features=[])
    profile.calculate(ref_data, data, mapping)

    dashboard = Dashboard(tabs=[DataDriftTab(), RegressionPerformanceTab(verbose_level=0)])
    dashboard.calculate(ref_data, data, mapping)
    return json.loads(profile.json()), dashboard


@task
def save_report(result):
    """Save evidendtly profile for ride prediction to mongo server"""

    client = MongoClient(MONGO_CLIENT_ADDRESS)
    collection = client.get_database(MONGO_DATABASE).get_collection(REPORT_COLLECTION)
    collection.insert_one(result)
