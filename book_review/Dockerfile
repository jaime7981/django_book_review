FROM python:3.10-slim-buster

ENV PYTHONBUFFERED 1
WORKDIR /django_app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
RUN apt-get update && apt-get install curl build-essential -y
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - 
RUN apt install nodejs -y
RUN npm install -g npm@latest

ADD . /django_app

#RUN npm install tailwindcss postcss-cli autoprefixer cross-env
# RUN npm i -g rimraf cross-env tailwindcss postcss
# RUN npm install --save-dev postcss-import postcss-nested postcss-simple-vars

RUN npm install --prefix /django_app/theme/static_src && npm run --prefix /django_app/theme/static_src build
