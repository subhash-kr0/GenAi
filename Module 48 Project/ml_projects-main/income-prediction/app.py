from flask import Flask, render_template, jsonify, request, send_file
from src.exception import CustomException
from src.logger import logging as lg
import os,sys

from src.pipeline.train_pipeline import TraininingPipeline
from src.pipeline.predict_pipeline import PredictionPipeline

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify("home")


@app.route("/train")
def train_route():
    try:
        train_pipeline = TraininingPipeline()
        train_pipeline.run_pipeline()

        return "Training Completed."

    except Exception as e:
        raise CustomException(e,sys)

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    
    try:
        if request.method == 'POST':
            input_data = dict(request.form.items())

            print(input_data)

            pred_pipe = PredictionPipeline()
            prediction = pred_pipe.run_pipeline(input_data)

            return render_template("prediction.html", context=str(prediction))


        else:
            return render_template("prediction.html")

    except Exception as e:
        raise CustomException(e,sys)
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug= True)