#IMPORTING LIBRARIES
import numpy as np
import pandas as pd
import mlflow
from prefect import flow, task, get_run_logger

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("recommender")