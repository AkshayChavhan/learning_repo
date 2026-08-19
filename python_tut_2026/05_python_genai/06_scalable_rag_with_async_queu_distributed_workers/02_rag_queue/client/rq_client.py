from redis import Redis    # For connecting to Redis  command to install redis "pip install redis"
from rq import Queue        # For creating a queue command to install rq "pip install rq"
# to freeze the requirements pip freeze > requirements.txt

queue = Queue(connection=Redis(
    host='localhost',
    port=6379,
    db=0
))