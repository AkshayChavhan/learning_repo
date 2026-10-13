# Image for the "backend" service. Compose builds it because of `build: .`
FROM node:20.17.0-alpine3.19

WORKDIR /home/app

# deps first, so a code-only change doesn't re-run npm install (layer cache)
COPY package.json package-lock.json ./
RUN npm install

COPY index.js ./

EXPOSE 8000

CMD ["npm", "start"]
