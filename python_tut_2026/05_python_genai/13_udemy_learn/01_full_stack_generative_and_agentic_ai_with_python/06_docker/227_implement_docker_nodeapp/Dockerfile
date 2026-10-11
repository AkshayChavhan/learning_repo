# Base Image
FROM node:20.17.0-alpine3.19

WORKDIR /home/app

COPY package.json /home/app/package.json
COPY package-lock.json /home/app/package-lock.json

RUN npm install

# Copying the source code to docker image

COPY index.js /home/app/index.js

# EXPOSE 8080
#  To run the container, we need to specify the command to run the application
CMD ["node", "start"]