from fastapi import APIRouter

from app.api.routes.contacts import router as contacts_router

api_router = APIRouter()
api_router.include_router(contacts_router)
