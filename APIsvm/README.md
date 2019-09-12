# SkLearn Model of ECG arrhythmia classification SVM with Flask as Web App 

------------------

## Getting started in 10 minutes

- Clone this repo 
- Install requirements
- Run the script
- Send an POST HTTP request with a ZIP file that contains ECG signal files (.txt) to http://localhost:5000
- Done! 


------------------

## Docker Installation

### Build and run an image for keras-application pretrained model 
```shell
$ cd APIsvm
$ docker build -t SVM_flask_app .
$ docker run -d -p 5000:5000 SVM_flask_app 
```


## Local Installation

### Clone the repo
```shell
$ git clone https://github.com/IslaBen/HeartBeat.git
cd APIsvm
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

Python 3.4+ are supported and tested.

```shell
$ python SVM_server.py
```
