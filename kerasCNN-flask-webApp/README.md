# Keras Model of ECG arrhythmia classification using a 2-D convolutional neural network with Flask as Web App 

------------------

## Getting started in 10 minutes

- Clone this repo 
- Install requirements
- Run the script
- Send an POST HTTP request with a ZIP file that contains ECG images beats (128x128x1) to http://localhost:5000
- Done! 


------------------

## Docker Installation

### Build and run an image for keras-application pretrained model 
```shell
$ cd kerasCNN-flask-webApp
$ docker build -t keras_flask_app .
$ docker run -d -p 5000:5000 keras_flask_app 
```


## Local Installation

### Clone the repo
```shell
$ git clone https://github.com/mtobeiyf/kerasCNN-flask-webApp.git
```

### Install requirements

```shell
$ pip install -r requirements.txt
```

Make sure you have the following installed:
- Werkzeug
- Flask
- numpy
- Keras
- gevent
- pillow
- h5py
- tensorflow
- shutil
- glob

### Run with Python

Python 2.7 or 3.5+ are supported and tested.

```shell
$ python app.py
```
### Set up Nginx

To redirect the traffic to your local app.
Configure your Nginx `.conf` file.
```
server {
    listen  80;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}
```
