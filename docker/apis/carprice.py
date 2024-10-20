import joblib
import pandas as pd
import numpy as np


# Add logging

def predictPrice(carlength, carwidth, horsepower, brandavg, averagempg):
    try:
        model = joblib.load("models/carprice.joblib")
                
        X_submit = pd.DataFrame({
            'carlength': [float(carlength)],
            'carwidth': [float(carwidth)],
            'horsepower': [float(horsepower)],
            'brandavg': [float(brandavg)],
            'averagempg': [float(averagempg)]
        })
        predicted_price = 10**model.predict(X_submit)[0]
        return int(predicted_price)
    except Exception as e:
        raise e
