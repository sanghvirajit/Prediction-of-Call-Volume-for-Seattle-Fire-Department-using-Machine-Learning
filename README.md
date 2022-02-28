# niologic-GmbH

# Prediction of Call Volume for Seattle Fire Department using Machine Learning

## Business case

Dispatching emergency calls in a city is challenging: There are large variations over a year, saison
and especially time of day. Someone has to decide how many dispatchers are on duty for every day.
Hence, we are looking for a model, which can predict the call volume for each day of the year and
each hour of the day.

A comparison study has been performed to understand which ML algorithm suits best to the dataset.

Seattle-Real-Time-Fire-911-Calls real time dataset is used which can be available at https://data.seattle.gov/Public-Safety/Seattle-Real-Time-Fire-911-Calls/kzjm-xkqj.

## Directory Structure

```scala
│   Dockerfile
│   model.bin
│   Pipfile
│   Pipfile.lock
│   predict.py
│   predict_docker.py
│   README.md
│   Requirements.txt
│   train.py
│
├───Data
│       hourly_data.csv
│       monthly_data.csv
│       processed_data.csv
│       Seattle_Real_Time_Fire_911_Calls.7z
│
├───Images
│       call_volume_month.png
│       call_volume_week.png
│       filename.png
│
└───Notebooks
    │   01_Date_processing_and _EDA.ipynb
    │   02_BaselineModels.ipynb
    │   03_ML_Modeling.ipynb
    │   04_Prophet_model.ipynb
    │   05_Model_Loading_and_Predicting.ipynb
    │   model_lightgbm.bin
```

### Approach to the problem

This problem is a Time series forecasting problem and was approached in 3 ways.

1. **In the first step a baseline model was developed using Persistence Algorithm (the “naive” forecast).**
   
   A baseline in performance gives us an idea of how well all other models will actually perform on our problem.
   
   The equivalent technique for use with time series dataset is the persistence algorithm. The persistence algorithm uses the value at the previous time step (t-1) to predict      the expected outcome at the next time step (t+1).
   
2. **In the second step machine learning models like decision tree and gradient boosting alogirthms were used.**

3. **In the third step Facebooks's Prophet model is used.**

    Prophet is designed for analyzing time series with daily observations that display patterns on different time scales. Prophet is robust to missing data and shifts in the         trend, and typically handles outliers well. It also has advanced capabilities for modeling the effects of holidays on a time-series and implementing custom changepoints, but I   sticked to the basics to get a model up and running.
  
    For more information on Prophet, readers can consult the official documentation on https://facebook.github.io/prophet/docs/quick_start.html.
  
  Though the main focus was on the machine learning models to stick with the guidelines of the project.
  Baseline models and Prophet models were build only in terms of comparision.
  
## Steps Involved

**Step 1** - Data Processing : Cleaning and Transforming Raw Data into the Understandable Format

**Step 2** - Profiling : Data profiling is the process of examining the data available from an existing information source (e.g. a database or a file) and collecting statistics or informative summaries about that data.

**Step 3** - Exploratory Data Analysis - EDA: Finding insights from the Data

**Part 4** - Model Building: **Decision Tree, Gradient Boosting and Facebook's Prophet** - hyperparameter tuning, to find the best parameters.

**Part 5** - Selecting the best model.

**Part 6** - Deployment of the model locally using Docker container and Flask application.

## Requirements

```scala
Python 3.8
numpy: 1.22.2
pandas: 1.4.1
scikit-learn: 1.0.2
waitress: 2.0.0
flask: 2.0.3
lightgbm: 3.3.2
requests: 2.26.0
``` 
### EDA and feature importance

![hourly](https://user-images.githubusercontent.com/69073063/156017435-6604992a-9c00-4bfc-be5f-9712d2a924f5.png)

![filename](https://user-images.githubusercontent.com/69073063/156017460-5dc1706e-6c7b-4159-a4eb-1a094a34d7f9.png)

### Model Summary 

![model_summary](https://user-images.githubusercontent.com/69073063/155983832-618d6c56-6c23-4fcb-b000-6be03ec6191f.png)

### Input to the model

Model can predict the call volume for each day of the year and each hour of the day.

Model takes two types of inputs, date to get the total call volume on that particular date and date/time to get the call volume for any particular hour of the day.

In order to get the total call volume in a day, modify the input as date,

```scala
input_ = {
    'date': '2022-01-01'
}
```
In order to get the hourly call volume in a day, modify the input as datetime,

```scala
input_ = {
    'datetime': '2022-01-01 15:00:00'
}
```
Input_ can be modify in **predict_docker.py** file, which is used as a testing end point.

### Deployment of model

I worked on the project on Windows, so I used waitress to serve the flask applicaion in order to deploy the model. 

```scala
waitress-serve --listen=0.0.0.0:9696 predict:app
``` 

If linux is used to test the model, I would suggest to use gunicorn to serve the flask application.

```scala
gunicorn --bind=0.0.0.0:9696 predict:app
``` 
Changes in Pipfile and Dockerfile can be made as per the requirement.

## Commands to run the project locally

```scala
git clone https://github.com/sanghvirajit/niologic-GmbH.git
docker build -t call_volume .
docker run -it --rm -p 9696:9696 call_volume
python3 predict_docker.py
``` 
**Building a docker image will also run the train.py file.**

## Output

**1. Hourly Call Volume prediction**

Input:

   ```scala
   input_ = {
       'datetime': '2022-01-01 15:00:00'
   }
   ```

Expected output:

   ```scala
   {
       'Call Volume for 2022-01-01 15:00:00': 14.0
   }
   ```

**2. Daily Call Volume prediction**

Input:

   ```scala
   input_ = {
       'date': '2022-01-01'
   }
   ```

Expected output:

   ```scala
   {
       'Call Volume for 2022-01-01': 272.0
   }
   ```
  
## Plots
  
  **1. Plot comparing the actual (measured) call volume vs. predicted call volume for a month**
  
    
  ![call_volume_month](https://user-images.githubusercontent.com/69073063/155965801-e557fd7f-7838-4b3f-a4ab-1d315c4ff740.png)
  

  **2. Plot comparing the actual (measured) call volume vs. predicted call volume for a week**
  
    
  ![call_volume_week](https://user-images.githubusercontent.com/69073063/155965897-2d0e767c-867d-4739-87b9-3ce7cfbf35e3.png)


       
