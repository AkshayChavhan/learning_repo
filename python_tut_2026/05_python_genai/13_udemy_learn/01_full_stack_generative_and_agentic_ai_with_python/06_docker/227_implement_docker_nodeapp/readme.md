# Node Health App — Dockerized

## Install Docker

```bash
brew install --cask docker
```

Then open Docker Desktop once (Spotlight → "Docker") and wait for it to
say it's running — the `docker` CLI won't work until then.

## Build

```bash
docker build -t my-app .
```

## Run

```bash
docker run -d -p 8080:8080 --name my-app my-app npm start
curl http://localhost:8080/
```

## Shell into the container (optional)

```bash
docker run -it my-app sh
```

## Stop

```bash
docker stop my-app && docker rm my-app
```
