from datetime import datetime
import os

AWS_S3_BUCKET_NAME = "income-prediction"
MONGO_DATABASE_NAME = "income"

TARGET_COLUMN = "Income"

MODEL_FILE_NAME = "model"
MODEL_FILE_EXTENSION = ".pkl"

artifact_folder_name = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
artifact_folder = os.path.join("artifacts", artifact_folder_name)
