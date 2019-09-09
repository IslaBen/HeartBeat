FROM python:3.7.3-alpine

MAINTAINER Mecheref Adel Youcef "a.mecheref@esi-sba.dz"

COPY . /app

WORKDIR /app

EXPOSE 80

RUN apk add --no-cache python3-dev libstdc++ 

RUN apk add --no-cache g++ 

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

CMD ["python", "run.py"]