"""
Main API v1 router that includes all endpoint routers.

This module aggregates all API v1 routers and provides the main
entry point for version 1 of the API.
"""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router

# Create main API v1 router
api_router = APIRouter(prefix="/v1")

# Include all feature routers
api_router.include_router(auth_router)

# As new routers are created, include them here:
# api_router.include_router(users_router)
# api_router.include_router(seasons_router)
# api_router.include_router(rounds_router)
# etc.