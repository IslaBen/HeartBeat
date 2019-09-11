FROM python:3.6.8-slim-stretch

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install Werkzeug Flask numpy Keras gevent pillow h5py tensorflow


CMD [ "python" , "app.py"]

