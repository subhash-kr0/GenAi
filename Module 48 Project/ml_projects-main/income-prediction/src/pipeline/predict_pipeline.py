import shutil
import os, sys
import pandas as pd
from src.logger import logging

from src.exception import CustomException
import sys
from flask import request
from src.constant import *
from src.utils.main_utils import MainUtils

from dataclasses import dataclass


@dataclass
class PredictionFileDetail:
    prediction_output_dirname: str = "predictions"
    prediction_file_name: str = "predicted_file.csv"
    prediction_file_path: str = os.path.join(prediction_output_dirname, prediction_file_name)


class PredictionPipeline:
    def __init__(self):

        self.utils = MainUtils()
        self.prediction_file_detail = PredictionFileDetail()

    def predict(self, feature_values):
        try:
            model_path = self.utils.download_model(
                bucket_name=AWS_S3_BUCKET_NAME,
                bucket_file_name="model.pkl",
                dest_file_name="model.pkl",
            )

            model = self.utils.load_object(file_path=model_path)

            preds = model.predict(feature_values)

            return preds

        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self, feature_values: dict):
        try:

            input_df = pd.DataFrame([[values for values in feature_values.values()]],
                                    columns=[column_name for column_name in feature_values.keys()])

            input_df = self.utils.remove_unwanted_spaces(input_df)

            prediction = self.predict(input_df)
            predicted_income = '<=50K' if prediction == 0 else '>50K'

            return predicted_income

        except Exception as e:
            raise CustomException(e, sys)
