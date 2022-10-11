FROM python:3.10.7

WORKDIR /project

COPY . .

RUN pip install Flask flask-sqlalchemy


CMD ["python3","-m","flask","run","--host=0.0.0.0"]
