import pandas as pd
import pickle
import lightgbm as lgb

data = pd.read_csv("Data/processed_data.csv")

output_file = 'model.bin'

# Splitting the data

X_train = data[data['year'] < 2022]
y_train = X_train['call_counter']

del X_train['call_counter']
X_train = X_train.set_index('date')

# LightGBM model

model = lgb.LGBMRegressor(
                       num_leaves = 30,
                       max_depth = 6,
                       learning_rate = 0.1
    )

# Training the model

print("Training the model...")

def train(model, X_train, y_train):
    
    model = model.fit(X_train, y_train)
    
    return model

model = train(model, X_train, y_train)

# Saving the model

print("Saving the model...")

with open(output_file, 'wb') as f_out:
    pickle.dump((model), f_out)

print("Model saved successfully!")