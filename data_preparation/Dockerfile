FROM jjanzic/docker-python3-opencv

MAINTAINER Mecheref Adel Youcef "a.mecheref@esi-sba.dz"

COPY . /app

WORKDIR /app

EXPOSE 81


RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt


CMD ["python", "data_preparation.py"]