# Push a Docker image to Amazon ECR

**ECR** (Elastic Container Registry) is Docker Hub inside AWS. This folder builds a minimal
Node backend image and pushes it to a private ECR repository with the lecture's three
commands — login, tag, push — wrapped in a script that explains each one as it runs.

```text
   your laptop                                   AWS (ap-south-1)
   index.js ──docker build──► backend:latest ──docker push──► <account>.dkr.ecr.ap-south-1.amazonaws.com/backend
                                   │                                     │
                     docker tag gives it the ECR name            ECS pulls it from here (next lectures)
```

---

## 1. Prerequisites

| Need | Check | Get it |
|---|---|---|
| **Docker Desktop** running | `docker info` | `brew install --cask docker` |
| **AWS account** + an IAM user with ECR access | — | note 244 |
| **AWS CLI** configured | `aws sts get-caller-identity` prints your account id | `brew install awscli` then `aws configure` (access key, secret, region `ap-south-1`, output `json`) |
| **ECR repository** named `backend` in `ap-south-1` | ECR console → Repositories | console: Create repository → Private → `backend`, or `./push-to-ecr.sh --create` |

---

## 2. What's in this folder

| File | Role |
|---|---|
| `index.js` | Express server; `GET /` returns a health JSON with the port it listens on |
| `Dockerfile` | `node:20-alpine`, `npm install`, **`ENV PORT=8000`** + `EXPOSE 8000` (the lecture's tweak: port configurable at run time), `CMD ["npm","start"]` |
| `push-to-ecr.sh` | build → login → tag → push, printing every command. `--dry-run` only prints; `--create` makes the repo if missing |
| `.env.example` | copy to `.env` and fill in `AWS_ACCOUNT_ID` (and region/repo/tag) — `.env` is gitignored |
| `.dockerignore` | keeps `node_modules`, the script and env files out of the image |

---

## 3. Build and run locally first

```bash
docker build -t backend .
docker run -d -p 8000:8000 --name backend backend && sleep 2
curl localhost:8000
docker rm -f backend
```

```text
{"status":"success","message":"backend is healthy","port":8000,"image":"local"}
```

The port comes from `ENV PORT=8000` in the Dockerfile. Anything that runs the image can
override it — ECS will, and so can you:

```bash
docker run -d -e PORT=9000 -p 9000:9000 --name backend backend && sleep 2 && curl localhost:9000
```
```text
{"status":"success","message":"backend is healthy","port":9000,"image":"local"}
```

---

## 4. Push to ECR

```bash
cp .env.example .env          # then put your 12-digit account id in AWS_ACCOUNT_ID
./push-to-ecr.sh --dry-run    # see the exact commands first
./push-to-ecr.sh              # do it (add --create if the repository doesn't exist yet)
```

What the script runs, and what each line means:

| # | Command | Meaning |
|---|---|---|
| 1 | `docker build -t backend:latest .` | build the image locally |
| 2 | `aws ecr get-login-password --region ap-south-1 \| docker login --username AWS --password-stdin <account>.dkr.ecr.ap-south-1.amazonaws.com` | the CLI fetches a **temporary (12 h)** password and pipes it into `docker login` for your registry → `Login Succeeded` |
| 3 | `docker tag backend:latest <account>.dkr.ecr.ap-south-1.amazonaws.com/backend:latest` | give the image its ECR name. Nothing is copied — same image id, second name |
| 4 | `docker push <account>.dkr.ecr.ap-south-1.amazonaws.com/backend:latest` | upload → `latest: digest: sha256:… size: …` |

These are the same commands the ECR console shows under **View push commands**, filled in
from your `.env` instead of by hand.

### The repository URI, decoded

```text
123456789012.dkr.ecr.ap-south-1.amazonaws.com/backend:latest
────────────  ───────────────────────────────  ───────  ──────
account id    registry host for your region    repo     tag
```

Docker Hub was `docker.io/<username>/node-application`; ECR is the same shape with your
account id and region as the namespace.

### Verify

```bash
aws ecr describe-images --repository-name backend --region ap-south-1
```
or refresh the repository in the ECR console: tag, size, pushed-at time and digest.

---

## 5. Try the tag step without an AWS account

`docker tag` never contacts the registry, so this part of the lesson works offline:

```bash
docker tag backend:latest 123456789012.dkr.ecr.ap-south-1.amazonaws.com/backend:latest
docker images | grep backend
```
```text
123456789012.dkr.ecr.ap-south-1.amazonaws.com/backend   latest   8dab69e2dddf
backend                                                 latest   8dab69e2dddf   ← same image id
```

One image, two names. Only `docker push` needs the login.

---

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `aws: command not found` | AWS CLI not installed | `brew install awscli` |
| `Unable to locate credentials` / `InvalidClientTokenId` | CLI not configured, or wrong keys | `aws configure` (note 244) |
| `no basic auth credentials` on push | the 12-hour ECR login expired, or you never logged in | re-run step 2 (the script does it every time) |
| `name unknown: The repository with name 'backend' does not exist` | no ECR repo yet, or wrong region | create it in the console (region **ap-south-1**) or `./push-to-ecr.sh --create` |
| `denied: User … is not authorized to perform: ecr:…` | IAM user lacks ECR permissions | attach `AmazonEC2ContainerRegistryPowerUser` (or FullAccess) to the user |
| push is slow the first time | base layers are uploaded once | normal; later pushes send only changed layers |
| `AWS_ACCOUNT_ID is not set` | no `.env` | `cp .env.example .env` and fill it in |

---

## 7. Where this leaves you

```text
   ✅ AWS account + CLI linked          (note 244)
   ✅ image built and pushed to ECR     (this folder)
   ⬜ ECS cluster + task definition     (next)
   ⬜ run it as a service on ECS
```
