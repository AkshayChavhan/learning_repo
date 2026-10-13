# ECR — Pushing Your Image to Amazon's Registry

**ECR** (Elastic Container Registry) is Docker Hub, but inside AWS. You build the image on
your laptop, log Docker in to ECR using your AWS CLI credentials, tag the image with the
ECR address, and push. ECS will pull it from there in the next lectures.

---

## 1. The flow

```text
   your laptop                              AWS (ap-south-1)
   node.js code ──docker build──► image ──docker push──► ECR repository "backend"
                                                              │
                                                              └──► ECS pulls it (next lectures)
```

| Docker Hub (note 231) | ECR |
|---|---|
| `docker.io/<username>/node-application` | `<account-id>.dkr.ecr.<region>.amazonaws.com/backend` |
| `docker login` with Hub password | `docker login` with a password from the AWS CLI |
| public by default on free plan | **private** by default |
| fine for sharing with the world | better when the rest of your infra is in AWS |

---

## 2. Create the repository (console)

| Step | Where | What |
|---|---|---|
| 1 | AWS console, region set to **Mumbai `ap-south-1`** | search **ECR** → Elastic Container Registry |
| 2 | Repositories → **Create repository** | visibility: **Private** |
| 3 | name | `backend` |
| 4 | tag mutability, scanning | leave defaults → **Create** |

You get a repository URI like:

```text
123456789012.dkr.ecr.ap-south-1.amazonaws.com/backend
────────────  ───────────────────────────────  ───────
account id    registry host for your region    repo name
```

That URI **is** the image name you'll tag and push.

---

## 3. Build the image locally

Small Dockerfile tweak first, so the port is configurable:

```dockerfile
ENV PORT=8000
EXPOSE 8000
CMD ["npm", "start"]
```

```bash
docker build -t backend .
docker images
```

```text
REPOSITORY   TAG      IMAGE ID       SIZE
backend      latest   3f2a9c1b7d4e   ...
```

---

## 4. Push: the three commands

In the ECR console, click **View push commands** on your repository. It gives you exactly
these, already filled in with your account id and region.

### a. Log Docker in to ECR

```bash
aws ecr get-login-password --region ap-south-1 \
  | docker login --username AWS --password-stdin 123456789012.dkr.ecr.ap-south-1.amazonaws.com
```

```text
Login Succeeded
```

| Part | Meaning |
|---|---|
| `aws ecr get-login-password` | the AWS CLI (configured in note 244) fetches a temporary password |
| `\|` | pipes it straight into… |
| `docker login --username AWS --password-stdin <registry>` | …Docker, which logs in to your ECR registry |

The password is temporary (12 hours). Re-run this when a push says "no basic auth
credentials".

### b. Tag with the ECR name

```bash
docker tag backend:latest 123456789012.dkr.ecr.ap-south-1.amazonaws.com/backend:latest
```

Same rule as Docker Hub: the image must carry the registry's full name. `docker tag` adds
the name; nothing is copied.

### c. Push

```bash
docker push 123456789012.dkr.ecr.ap-south-1.amazonaws.com/backend:latest
```

```text
The push refers to repository [123456789012.dkr.ecr.ap-south-1.amazonaws.com/backend]
5f70bf18a086: Pushed
...
latest: digest: sha256:9a1c... size: 1234
```

Refresh the ECR console: the image is listed with tag, size, push time and digest.

---

## 5. Where you are now

```text
   ✅ AWS account + CLI linked         (note 244)
   ✅ image built and in ECR            (this note)
   ⬜ cluster + task definition         (next)
   ⬜ run it as a service on ECS
```

---

## Remember

| Term | One line |
|---|---|
| **ECR** | Amazon's private Docker registry |
| **repository URI** | `<account>.dkr.ecr.<region>.amazonaws.com/<repo>`; the image name you push to |
| **View push commands** | ECR console button that writes the login/tag/push commands for you |
| **`aws ecr get-login-password \| docker login`** | log Docker in to ECR with CLI credentials |
| **`docker tag backend <uri>:latest`** | give the local image its ECR name |
| **`docker push <uri>:latest`** | upload |
| **temporary login** | expires in 12 hours; re-run the login command |

> **If someone asks in an interview:** "How do you get an image into ECR?" Create a
> repository, authenticate Docker with `aws ecr get-login-password` piped into
> `docker login`, tag the image with the repository URI, and `docker push`. Same workflow
> as Docker Hub, with AWS credentials instead of a Hub account.
