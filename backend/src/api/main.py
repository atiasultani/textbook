from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.config.settings import settings
from src.api.v1 import textbook, chat, search, cohere
from src.api.v1.auth import router as auth_router
from src.auth.auth_handler import authenticate_user, create_access_token, Token
from src.services.auth_service import auth_middleware
import uvicorn
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url="/api/docs",  # Enable API documentation
    redoc_url="/api/redoc"
)

# Add authentication middleware
app.middleware("http")(auth_middleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, configure this properly
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(textbook.router, prefix=settings.api_v1_prefix, tags=["textbook"])
app.include_router(chat.router, prefix=settings.api_v1_prefix, tags=["chat"])
app.include_router(search.router, prefix=settings.api_v1_prefix, tags=["search"])
app.include_router(cohere.router, prefix=settings.api_v1_prefix, tags=["cohere"])
app.include_router(auth_router, prefix=settings.api_v1_prefix, tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Textbook RAG API", "status": "running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

@app.post("/token", response_model=Token, tags=["auth"])
async def login_for_access_token(username: str, password: str):
    """Authenticate user and return access token"""
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"General error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )