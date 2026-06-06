from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import devices, auth
from app.api.websocket.connection_manager import ConnectionManager
from app.api.websocket import command_handler, terminal_handler
from app.db.database import init_db
from app.config import settings
import logging

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("backend")

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()

# Wire manager into devices route
devices.set_manager(manager)
command_handler.set_manager(manager)
app.include_router(devices.router, prefix="/api/v1", tags=["devices"])
app.include_router(command_handler.router, prefix="/api/v1", tags=["commands"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])


@app.on_event("startup")
async def startup():
    init_db()
    logger.info(f"NeuroSync backend started on {settings.HOST}:{settings.PORT}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await command_handler.handle_agent_connection(websocket, manager)


@app.get("/")
async def root():
    return {"status": "NeuroSync running", "version": settings.VERSION}