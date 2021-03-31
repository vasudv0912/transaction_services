FROM python:3.7
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y nodejs \
    npm  
RUN npm install npm -g
RUN npm install pm2 -g
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
