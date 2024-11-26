import time
import redis
import json
import os
import requests
from logging import getLogger, basicConfig, INFO
from datetime import datetime, timedelta
basicConfig(level=INFO)
logger = getLogger(__name__)

redis_host = os.getenv('REDIS_HOST', 'redis_queue')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

def scale_instance():
    logger.info("A request has been made to scale the instance.")

def process_requests():
    while True:
        queue_length = redis_client.llen('request_queue')
        if queue_length > 0:
            message = redis_client.lpop('request_queue')
            if message:
                message = json.loads(message.decode('utf-8'))
                acces_module = requests.get('http://access_module:8002/')
                if acces_module.status_code != 200:
                    scale_instance()
                    if message['retries'] > 5:
                        logger.error(f"Request failed after 5 retries: {message}")
                        with open('data/failed_requests.jsonl', 'a') as file:
                            file.write(json.dumps(message) + '\n')
                        continue
                    message['retries'] = message.get('retries', 0) + 1
                    redis_client.rpush('request_queue', json.dumps(message))
                
                # if message take more than 5 seconds to process, discard it and send to failed_requests.jsonl
                timestamp = message.get('timestamp', 0)
                readable_time = datetime.fromtimestamp(timestamp)
                if datetime.now() > readable_time + timedelta(seconds=5):
                    logger.error(f"Request discarded after 5 seconds: {message}")
                    with open('data/failed_requests.jsonl', 'a') as file:
                        file.write(json.dumps(message) + '\n')
                    scale_instance()
                    continue
                
    
                requests.post('http://tourniquet:8001/open', json=message)
        else:
            time.sleep(0.1)  # Wait if the queue is empty

if __name__ == '__main__':
    process_requests()