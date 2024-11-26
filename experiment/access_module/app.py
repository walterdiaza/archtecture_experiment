from fastapi import FastAPI
import numpy as np



app = FastAPI()

@app.get("/")
async def root():  
     
    if np.random.rand() < 0.1:
        raise Exception("Error")
    return {"message": "ok"}
    
    