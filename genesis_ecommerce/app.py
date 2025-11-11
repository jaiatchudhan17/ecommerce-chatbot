from contextlib import asynccontextmanager

from fastapi import FastAPI

from genesis_ecommerce.api.v1 import router as v1_router
from genesis_ecommerce.db.core import init_db
from genesis_ecommerce.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Initializing database...")
    init_db()
    logger.info("✓ Database initialized")
    yield
    # Shutdown
    logger.info("Shutting down...")


app = FastAPI(
    title="Genesis E-commerce API",
    description="E-commerce platform with customer support bot",
    version="1.0.0",
    lifespan=lifespan,
)

# Include API routers
app.include_router(v1_router)
logger.info("✓ API routes registered")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Genesis E-commerce API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
