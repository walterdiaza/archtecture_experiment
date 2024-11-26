from fastapi import FastAPI, Request
import json

app = FastAPI()

@app.post("/open")
async def open_file(request: Request):
    body = await request.json()
    
    with open("/data/requests.jsonl", "a") as f:
        f.write(json.dumps(body) + "\n")
        
    print(f"Received request: {body}")
    
    return {"message": "Request received"}
        