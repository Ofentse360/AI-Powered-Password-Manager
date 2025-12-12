"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.init_db import init_database
# Import API routers
from app.api import auth, passwords, security, generator

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Password Manager API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows your React frontend (on port 5173) to talk to this backend (on port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"], # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and ML models on startup"""
    init_database()
    print(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} started successfully")

# --- 2. Register the router ---
# prefix="/api/auth" means all routes in auth.py will start with /api/auth
# tags=["Authentication"] groups them nicely in the auto-generated docs
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

# --- 3. Register the Passwords router ---
app.include_router(passwords.router, prefix="/api/passwords", tags=["Passwords"])

# --- 4. Register the Security Tools router ---
app.include_router(security.router, prefix="/api/security", tags=["Security Tools"])
# --- 5. Register the Password Generator router ---
app.include_router(generator.router, prefix="/api/generator", tags=["Generator"])
# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "status": "healthy",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}