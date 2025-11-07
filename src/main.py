import uvicorn
import sys

from pathlib import Path
from fastapi import FastAPI

from src.api.hotels import router as router_hotels


app = FastAPI(version="0.0.1.2")
app.include_router(router_hotels)

sys.path.append(str(Path(__file__).parent.parent))


