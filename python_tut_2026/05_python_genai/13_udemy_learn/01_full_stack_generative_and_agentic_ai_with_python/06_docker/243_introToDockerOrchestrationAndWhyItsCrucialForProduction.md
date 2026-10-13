# Docker Orchestration — Why You Need It in Production

Starting one container is easy. Keeping **many** containers healthy under real traffic is
not: scaling up, scaling down, replacing crashed ones, collecting logs. Doing that by hand
is a full-time job. Tools that do it for you are **orchestrators**: Kubernetes, AWS ECS,
Cloud Run. This section uses AWS ECS.

---

## 1. Deploying with what you know today

```text
   buy a $5 server (Ubuntu)
   └── install Docker engine
       └── docker pull <you>/my-node-app         (image pushed to Docker Hub earlier)
           └── docker run -itd --rm -p 8000:8000 <you>/my-node-app
               └── point api.com → server's public IP, port 8000
```

This works. One container, one server, a domain. Nothing wrong with it.

---

## 2. Then traffic grows

| What happens | What you do by hand |
|---|---|
| one container can serve maybe 100–200 users | run the command again: container 2 on port 8001 |
| two containers need a traffic splitter | install **nginx** as a load balancer, 50 / 50 |
| still growing | container 3 on 8002, update nginx to 33 / 33 / 33 |
| traffic drops at night | `docker stop` the idle containers, update nginx |
| traffic spikes again | start them again, update nginx |
| a container **crashes** | notice it, kill it, start a replacement, update nginx |
| need to debug | collect logs from every container into one place (e.g. Grafana) |

```text
   users ──► nginx ──┬──► container 1 (8000)   ✅
                     ├──► container 2 (8001)   ✅
                     └──► container 3 (8002)   ❌ crashed, who noticed?
```

Every row above is **you, manually, watching all day**. Not feasible for one person,
not feasible at all at scale.

---

## 3. That job has a name

Everything in the table is **orchestration**:

| Orchestration means | |
|---|---|
| **scale up** | add containers when load rises |
| **scale down** | remove containers when load falls |
| **self-heal** | detect a crashed container and replace it |
| **load balance** | spread traffic across the containers |
| **logs** | gather output from all containers in one place |
| **monitor** | know what each container is doing |
| **deploy / roll back** | ship a new version safely, undo if it breaks |

You were the orchestrator. Now hand the job to a tool.

---

## 4. The tools

| Orchestrator | By | Notes |
|---|---|---|
| **Kubernetes** | open source (Google origin) | the big one, runs anywhere |
| **AWS ECS** (Elastic Container Service) | Amazon | **this course's choice** |
| Cloud Run | Google Cloud | simpler, serverless containers |
| Docker Swarm | Docker | built in, less used now |

You give the tool a **configuration** ("run 3 copies of this image, restart on crash,
scale between 2 and 10"), and it does the watching and acting for you.

### Why AWS in this course

- Industry standard. Most serious companies run on it, so it's what jobs ask for.
- The **concepts transfer**. Learn ECS and Kubernetes or Google Cloud feel familiar.
  Same ideas, different names.

---

## What this section will cover

Load balancing, CDNs, health checks, rollbacks, deployment strategies, log collection.
By the end: deploy containers on AWS, keep them running, scale them, read their logs.

---

## Remember

| Term | One line |
|---|---|
| **orchestration** | managing many containers: scale, heal, balance, log, monitor |
| **load balancer** | splits traffic across containers (nginx, or cloud-provided) |
| **self-healing** | crashed container replaced automatically |
| **orchestrator** | the tool that does it: Kubernetes, ECS, Cloud Run |
| **ECS** | AWS Elastic Container Service, used in this course |
| **manual = pain** | every scaling or crash is a human action otherwise |

> **If someone asks in an interview:** "What is container orchestration?" Automating the
> management of many containers: scheduling them onto servers, scaling up and down with
> load, restarting or replacing failed ones, load balancing traffic, and centralising logs
> and health checks. Kubernetes and AWS ECS are the common orchestrators.
