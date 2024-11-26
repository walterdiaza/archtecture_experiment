from fastapi import FastAPI, Request
import time
import redis
import json
import os

app = FastAPI()

redis_host = os.getenv('REDIS_HOST', 'redis_queue')
redis_port = int(os.getenv('REDIS_PORT', 6379))

redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

@app.post("/request")
async def receive_request(request: Request):
    data = await request.json()
    timestamp = time.time()
    message = json.dumps({'timestamp': timestamp, 'data': data, 'retries': 0})
    redis_client.rpush('request_queue', message)
    return {'message': 'Request received'}