"""
FastAPI main application entry point.

This module creates and configures the FastAPI application instance
for the Golf League Management System.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI application instance
app = FastAPI(
    title="Golf League Management API",
    description="Backend API for managing golf league operations, tournaments, and member data",
    version="0.1.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)

# Configure CORS for development
# TODO: Update origins for production deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "healthy", "message": "Golf League Management API is running"}


@app.get("/")
async def root():
    """Root endpoint redirect to API documentation."""
    return {"message": "Golf League Management API", "docs": "/api/v1/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)