import pandas as pd
import pickle
from flask import Flask
from flask import request
from flask import jsonify

print("Loading the model...")

input_file = 'model.bin'

with open(input_file, 'rb') as f_in: 
    model = pickle.load(f_in)

print("Preparing the input...")

app = Flask('call_volume')

def prepare_input(input_):
    key, value = list(input_.items())[0]

    from datetime import timedelta
    df = pd.DataFrame([input_])
    df['datetime'] = pd.to_datetime(df[key])

    if (key == 'date'):
        df = pd.DataFrame(
            {'datetime': pd.date_range(df['datetime'].dt.date[0], df['datetime'].dt.date[0] + timedelta(days=1),
                                       freq='1H', closed='left')}
        )

    return df

def create_features(df):
    
    df["year"]           = df["datetime"].apply(lambda time: time.year)
    df["day_of_month"]   = df["datetime"].apply(lambda time: time.day)
    df["month"]          = df["datetime"].apply(lambda time: time.month)
    df["hour"]           = df["datetime"].apply(lambda time: time.hour)
    df['day_of_year']    = df['datetime'].apply(lambda time: time.dayofyear)
    df['day_of_week']    = df['datetime'].apply(lambda time: time.dayofweek)
    df['week_of_year']   = df['datetime'].apply(lambda time: time.weekofyear)
    
    del df['datetime']
    
    return df

@app.route('/predict', methods=['POST'])
def predict():

    input_ = request.get_json()

    key, value = list(input_.items())[0]

    df = prepare_input(input_)
    
    df = create_features(df)

    predicted = model.predict(df).round()

    result = {
        'Call Volume for {}'.format(value): float(predicted.sum())
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
