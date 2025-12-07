"""
Smart Government FastAPI Application
============================
Main entry point for the BioSync recommendation engine

Developer: Ghadeer - AI/ML Engineer
Date: December 2025
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
import uvicorn

# Create FastAPI application
app = FastAPI(
    title="Smart Government API",
    description=(
        " Smart Recommendation Engine for Government Services\n\n"
        "**Features:**\n"
        "- AI-powered priority scoring\n"
        "- 4-factor analysis (Urgency, Seasonality, Importance, Activity)\n"
        "- Personalized SMS alerts\n"
        "- Real-time recommendations\n\n"
        "**Developer:** Ghadeer (AI/ML Engineer)\n"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Ghadeer",
        "email": "Ghadeer.55.s@outlook.com"  # Update with your email
    },
    license_info={
        "name": "MIT"
    }
)

# CORS Configuration
# Allows frontend (Reem's React app) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify Reem's domain only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.get("/")
async def root():
    """
    Root endpoint - Welcome message
    
    Returns:
        dict: Welcome message and quick links
    """
    return {
        "message": "Smart Government API is running!",
        "tagline": "Smart recommendations for government services",
        "status": "operational",
        "endpoints": {
            "interactive_docs": "/docs",
            "api_info": "/api",
            "health_check": "/api/health",
            "recommendations": "/api/recommendations (POST)"
        },
        "quick_start": {
            "1": "Visit /docs for interactive API documentation",
            "2": "POST to /api/recommendations with user + services data",
            "3": "Get smart recommendations ranked by priority"
        },
        "developer": "Ghadeer - AI/ML Engineer",
    }


# Run application directly
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )