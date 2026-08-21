from fastapi import FastAPI, HTTPException, Query
from client.rq_client import queue
from queues.worker import process_query

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Server is running"}

@app.post("/chat")
def chat(query: str = Query(... , description="The query to search the database")):
    job = queue.enqueue(process_query, query)
    return {"status": "Chat is running", "job_id": job.id}

@app.get("/chat/{job_id}")
def get_chat(job_id: str):
    job = queue.fetch_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"No job with id {job_id}")

    # get_status() -> queued | started | finished | failed | deferred | scheduled
    status = job.get_status()

    # NOTE: in rq 2.x return_value is a METHOD, not a property.
    # Writing `job.return_value` hands back the bound method itself, which
    # FastAPI silently serialises as {} - you get 200 OK and no answer.
    result = job.return_value() if status == "finished" else None

    return {"status": status, "job_id": job.id, "result": result}
