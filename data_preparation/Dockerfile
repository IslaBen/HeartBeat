FROM python:3.7.3-alpine

MAINTAINER Mecheref Adel Youcef "a.mecheref@esi-sba.dz"

COPY . /app

WORKDIR /app

EXPOSE 81

RUN pip install -r requirements.txt

VOLUME . /app

CMD ["python", "data_preparation.py"]