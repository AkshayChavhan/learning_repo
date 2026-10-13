FROM node:20.17.0-alpine3.19

WORKDIR /home/app

# deps first so a code-only change doesn't re-run npm install (layer cache)
COPY package.json package-lock.json ./
RUN npm install --omit=dev

COPY index.js ./

# The tweak from the lecture: make the port configurable.
# ENV sets a default inside the container; ECS (or `docker run -e PORT=...`) can override it.
ENV PORT=8000
EXPOSE 8000

CMD ["npm", "start"]
