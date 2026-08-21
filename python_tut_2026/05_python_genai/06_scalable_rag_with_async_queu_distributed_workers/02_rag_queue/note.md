Valkey + Python RQ Setup Guide

This guide shows how to use Valkey with Python RQ (Redis Queue) to run background jobs.

Note: We are using Valkey instead of Redis. Valkey is Redis-compatible, so RQ can work with it.

1. Create Valkey with Docker Compose

Create a file named docker-compose.yml:

services:
  valkey:
    image: valkey/valkey:latest
    container_name: valkey
    ports:
      - "6379:6379"


Start Valkey:

docker compose up -d


Check if the container is running:

docker ps


You should see the valkey container running on port 6379.

To stop it:

docker compose down

2. Why Redis/Valkey and RQ?

Suppose a user sends a chat message. Processing the message may take some time.

If we process it directly inside the API:

User
  |
  v
FastAPI
  |
  |---- Process message
  |
  v
Result


The user has to wait until the processing is finished.

Instead, we can put the work into a queue:

User
  |
  v
FastAPI
  |
  |----> Valkey Queue
  |           |
  |           v
  |       RQ Worker
  |           |
  |           v
  |      Process message
  |
  v
Response


This allows the API to accept the request without doing the heavy work itself.

3. FastAPI + RQ + Valkey Flow

In our application, the FastAPI server will provide an API endpoint:

POST /chat


The client sends:

{
  "message": "Hello"
}


The overall flow looks like this:

                    POST /chat
User/Frontend ----------------------> FastAPI
                                         |
                                         | Add job
                                         v
                                      Valkey
                                     [ Queue ]
                                         |
                                         | Get job
                                         v
                                    RQ Worker
                                         |
                                         | Process message
                                         v
                                       Result


A simple request flow can be:

Client
  |
  | POST /chat
  | { "message": "Hello" }
  v
FastAPI
  |
  | enqueue job
  v
Valkey
  |
  | job waiting
  v
RQ Worker
  |
  | process message
  v
Result

4. Why Redis/Valkey and RQ?
Valkey

Valkey acts as the storage/queue.

Valkey
   |
   +-- Job 1
   +-- Job 2
   +-- Job 3

RQ

RQ manages the jobs and workers.

RQ
 |
 +-- Queue
 |
 +-- Worker

FastAPI

FastAPI provides the API that the frontend/client calls.

POST /chat
      |
      v
FastAPI
      |
      v
RQ Queue

5. Install RQ

Install RQ:

pip install rq


Save the installed packages:

pip freeze > requirements.txt


Use requirements.txt as the conventional filename.

6. Project Structure

We will create two folders:

project/
│
├── client/
│   └── rq_client.py
│
├── queues/
│   └── worker.py
│
├── docker-compose.yml
└── requirements.txt

client/

The client folder contains code that connects to Valkey and adds jobs to the queue.

queues/

The queues folder contains the RQ workers that take jobs from the queue and execute them.

7. Smallest Example
Client

Create client/rq_client.py:

from redis import Redis
from rq import Queue

redis_connection = Redis(host="localhost", port=6379)

queue = Queue(connection=redis_connection)

queue.enqueue(print, "Hello from RQ!")


Run it:

python client/rq_client.py


The client puts this job into Valkey:

print("Hello from RQ!")


The job is now waiting in the queue.

8. Start the Worker

Create queues/worker.py:

from redis import Redis
from rq import Worker, Queue

redis_connection = Redis(host="localhost", port=6379)

queue = Queue(connection=redis_connection)

worker = Worker([queue], connection=redis_connection)

worker.work()


Start the worker:

python queues/worker.py


The worker now waits for jobs.

When the client adds:

print("Hello from RQ!")


the worker takes the job and executes it.

9. FastAPI Server

Now we can put the queue behind a FastAPI endpoint.

Client
  |
  | POST /chat
  | { "message": "Hello" }
  v
FastAPI Server
  |
  | enqueue()
  v
Valkey
  |
  | Job
  v
RQ Worker
  |
  | Process message
  v
Result


For example:

POST /chat
{
    "message": "Hello"
}


FastAPI receives the message and creates an RQ job.

The worker processes the job in the background.

The application can then provide a result endpoint, for example:

GET /result/{job_id}


The complete flow becomes:

                 POST /chat
Client ------------------------------> FastAPI
  |                                      |
  |                                      | enqueue job
  |                                      v
  |                                   Valkey
  |                                  [ Queue ]
  |                                      |
  |                                      | job
  |                                      v
  |                                  RQ Worker
  |                                      |
  |                                      | process
  |                                      v
  |                                    Result
  |                                      |
  |                                      |
  |       GET /result/{job_id}            |
  +--------------------------------------+
                 |
                 v
              Response

Simple idea
POST /chat
     |
     v
Create Job
     |
     v
Return job_id
     |
     v
Worker processes job
     |
     v
GET /result/{job_id}
     |
     v
Get result


FastAPI handles HTTP requests, RQ manages background jobs, Valkey stores the jobs, and the RQ worker executes them.

10. Important Points
FastAPI provides the API endpoints.
POST /chat receives the user's message.
RQ puts the work into a background queue.
Valkey stores the queued jobs.
RQ Worker takes jobs from Valkey and executes them.
The worker can process the message without blocking the FastAPI server.
A job_id can be used to check the result later.
GET /result/{job_id} can return the job result.
Multiple workers can process multiple jobs.
In one sentence

Client → FastAPI → RQ → Valkey → RQ Worker → Result → /result/{job_id}