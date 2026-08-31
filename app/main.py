from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_tables
from app.routes import router
from orchestrator.graph import workflow_router

load_dotenv()

@asynccontextmanager
async def lifespan(_: FastAPI):
	create_tables()
	yield


app = FastAPI(title="Agentic URL Shortener", version="1.0.0", lifespan=lifespan)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/health")
def health() -> dict[str, str]:
	return {"status": "ok"}


app.include_router(router)
app.include_router(workflow_router)
