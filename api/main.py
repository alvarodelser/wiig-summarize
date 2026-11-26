# wiig-summarize/api/main.py
"""Profile-driven summarization: each profile is a prompt and the JSON schema
its answer must follow (article, entity/relation descriptions, procurement
requirements and criteria...). An extractive pre-pass (sumy) trims long inputs;
the writing is done by Ollama (ollama_high on wiig-net). No model here, no GPU."""
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response

from api.warmth import get_missing, mark_warm

logging.basicConfig(
    level=os.environ.get("NLP_LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
log = logging.getLogger("wiig_summarize")


@asynccontextmanager
async def lifespan(app: FastAPI):
    mark_warm("summarize")      # nothing to preload: the model is in Ollama
    log.info("wiig-summarize ready")
    yield
    log.info("wiig-summarize shutting down")


app = FastAPI(title="wiig-summarize", lifespan=lifespan)


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/readyz")
def readyz(response: Response) -> dict:
    missing = get_missing({"summarize"})
    if missing:
        response.status_code = 503
        return {"status": "warming", "missing": missing}
    return {"status": "ready"}


from api.routers import summarize as _summarize_router  # noqa: E402
app.include_router(_summarize_router.router)
