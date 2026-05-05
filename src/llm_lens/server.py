from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llm_lens.core import get_records, get_stats

app = FastAPI(title="llm-lens")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/calls")
def calls():
    return get_records()

@app.get("/stats")
def stats():
    return get_stats()

@app.get("/health")
def health():
    return {"status": "ok"}
