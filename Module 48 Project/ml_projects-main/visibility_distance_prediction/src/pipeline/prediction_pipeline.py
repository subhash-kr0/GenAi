import shutil
import os,sys
import pandas as pd
from src.logger import logging

import sys
from src.cloud_storage.aws_syncer import S3Sync
from flask import request
from src.utils.main_utils import MainUtils
from src.constant import *
from src.exception import VisibilityException

from dataclasses import dataclass
        
        
@dataclass
class PredictionPipelineConfig:
    model_path = os.path.join("artifacts","prediction_model","model.pkl")




class PredictionPipeline:
    def __init__(self, request: request):

        self.request = request  
        self.s3_sync = S3Sync()     
        self.utils = MainUtils()
        self.prediction_pipeline_config = PredictionPipelineConfig() 


    def download_model(self):
        try:
            self.s3_sync.sync_folder_from_s3(
                folder= os.path.dirname(self.prediction_pipeline_config.model_path),
                 aws_bucket_name= AWS_S3_BUCKET_NAME )
            
            return self.prediction_pipeline_config.model_path
            
        except Exception as e:
            raise VisibilityException(e,sys)
        
        
    def run_pipeline(self):
        try:
            data = dict(self.request.form.items())
            values = data.values()


            model_path = self.download_model()

            model = self.utils.load_object(file_path=model_path)

            prediction = model.predict([list(values)])

            return prediction


        except Exception as e:
            raise VisibilityException(e,sys)
            
        

 
        

        