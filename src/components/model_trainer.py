import os
import numpy as np
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
import sys

from catboost import CatBoostRegressor
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
#from xgboost import XGBRegressor
from sklearn.linear_model import Ridge,Lasso

from src.utils import save_object
from src.utils import evaluate_model

@dataclass
class ModelTrainerConfig:
    train_model_file_path = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()


    def initiate_model_trainer(self,train_arr,test_arr):
        try:
            logging.info('splitting training and test input data')
            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            models = {
            "Linear Regression": LinearRegression(),
            "Lasso": Lasso(),
            "Ridge": Ridge(),
            "K-Neighbors Regressor": KNeighborsRegressor(),
            "Decision Tree": DecisionTreeRegressor(),
            "Random Forest Regressor": RandomForestRegressor(),
            "AdaBoost Regressor": AdaBoostRegressor(),
            'Gradient Boost Regressor':GradientBoostingRegressor()
            }

            params = {

            "Linear Regression": {
                "fit_intercept": [True, False]
            },

            "Lasso": {
                "alpha": [0.1, 1.0]
            },

            "Ridge": {
                "alpha": [0.1, 1.0]
            },

            "K-Neighbors Regressor": {
                "n_neighbors": [3, 5],
                "weights": ["uniform", "distance"]
            },

            "Decision Tree": {
                "max_depth": [None, 5, 10],
                "min_samples_split": [2, 5]
            },

            "Random Forest Regressor": {
                "n_estimators": [100],
                "max_depth": [None, 10],
                "min_samples_split": [2, 5]
            },
            "AdaBoost Regressor": {
                "n_estimators": [50, 100],
                "learning_rate": [0.05, 0.1]
            },

            "Gradient Boost Regressor": {
                "n_estimators": [100],
                "learning_rate": [0.05, 0.1],
                "max_depth": [3, 5]
            }
            }

            model_report:dict = evaluate_model(x_train = x_train,y_train=y_train,x_test=x_test,y_test=y_test,models = models,param=params)
            best_model_score = max(list(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
                ]
            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info("best model found on both trainig and test data")

            save_object(
                file_path=self.model_trainer_config.train_model_file_path,
                obj = best_model)

            predicted = best_model.predict(x_test)
            r2_square = r2_score(y_test,predicted)
            return f"{r2_square} : {best_model_name}"
            
        except Exception as e:
            raise CustomException(e,sys)
