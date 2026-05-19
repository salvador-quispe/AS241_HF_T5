from fastapi import FastAPI

app = FastAPI(title="AS241_HF_T5 API")

@app.get("/")
def root():
    return {"message": "API running"}
