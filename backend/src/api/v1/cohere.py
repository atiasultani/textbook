from fastapi import APIRouter, Depends, HTTPException
from src.auth.auth_handler import get_current_user
from src.services.cohere_service import CohereConfig
from src.services.cohere_service import CohereService

router = APIRouter()

# Initialize Cohere service
cohere_service = CohereService()

@router.get("/cohere/config", response_model=CohereConfig)
async def get_cohere_config(current_user=Depends(get_current_user)):
    """Get Cohere integration configuration (requires authentication)"""
    try:
        config = cohere_service.get_config()
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting Cohere config: {str(e)}")