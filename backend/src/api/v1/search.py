from fastapi import APIRouter, HTTPException
from src.models.embeddings import SearchRequest, SearchResponse
from src.services.rag_service import search_content

router = APIRouter()

@router.post("/textbook/search", response_model=SearchResponse)
async def textbook_search(request: SearchRequest):
    """Search textbook content"""
    try:
        results = await search_content(request.query, request.top_k)
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching content: {str(e)}")