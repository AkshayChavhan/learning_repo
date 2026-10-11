# Base Image

FROM ubuntu

RUN apt-get update
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_18.x -o /tmp/nodesource_setup.sh
RUN bash /tmp/nodesource_setup.sh
RUN apt-get install -y nodejs


# Copying the source code to docker image

COPY index.js /home/app/index.js
COPY package.json /home/app/package.json
COPY package-lock.json /home/app/package-lock.json

WORKDIR /home/app

RUN npm install

