FROM python:3.8.12-slim

RUN pip install pipenv

WORKDIR /app

COPY Data/processed_data.csv ./Data/processed_data.csv
COPY ["Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y install curl
RUN apt-get install libgomp1

COPY ["train.py", "predict.py", "model.bin", "./"]

RUN python3 train.py

EXPOSE 9696

ENTRYPOINT ["waitress-serve", "--listen=0.0.0.0:9696", "predict:app"]
# ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]