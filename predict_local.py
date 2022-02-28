import pandas as pd
import pickle

print("Loading the model...")

input_file = 'model.bin'

with open(input_file, 'rb') as f_in:
    model = pickle.load(f_in)

print("Preparing the input...")

input_ = {
    'date': '2022-01-01'
}

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
    df["year"] = df["datetime"].apply(lambda time: time.year)
    df["day_of_month"] = df["datetime"].apply(lambda time: time.day)
    df["month"] = df["datetime"].apply(lambda time: time.month)
    df["hour"] = df["datetime"].apply(lambda time: time.hour)
    df['day_of_year'] = df['datetime'].apply(lambda time: time.dayofyear)
    df['day_of_week'] = df['datetime'].apply(lambda time: time.dayofweek)
    df['week_of_year'] = df['datetime'].apply(lambda time: time.weekofyear)

    del df['datetime']

    return df

def predict(model, input_):

    key, value = list(input_.items())[0]

    df = prepare_input(input_)

    df = create_features(df)

    predict = model.predict(df).round()

    return print('Call Volume for given {}'.format(key) + ': ' + str(predict.sum()))

print("Predicting the call volume...")

predict(model, input_)
