from fastapi import FastAPI
app = FastAPI(title="Real-time Async Stack")

@app.get("/")
def read_root():
    return {"Hello": "From Docker!"}