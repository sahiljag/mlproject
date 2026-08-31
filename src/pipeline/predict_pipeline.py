from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import sys
import traceback
from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import PredictPipeline,CustomData

application = Flask(__name__)

app = application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        try:
            data = CustomData(gender=request.form.get('gender'),
                    race_ethnicity=request.form.get('ethnicity'),
                    parental_level_of_education=request.form.get('parental_level_of_education'),
                    lunch=request.form.get('lunch'),
                    test_preparation_course=request.form.get('test_preparation_course'),
                    reading_score=float(request.form.get('reading_score')),
                    writing_score=float(request.form.get('writing_score'))
                )
            pred_df = data.get_data_as_df()
            print(pred_df, flush=True)

            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            return render_template('home.html',results=results[0])
        except Exception:
            print("PREDICTION ERROR:", flush=True)
            traceback.print_exc(file=sys.stdout)
            sys.stdout.flush()
            raise

if __name__ == "__main__":
    app.run(host='0.0.0.0')