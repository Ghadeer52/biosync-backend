"""
API Endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List
from app.models.schemas import (
    RecommendationRequest,
    User,
    Service
)
from app.core.recommender import SmartRecommender

router = APIRouter(prefix="/api", tags=["Smart Government"])

recommender = SmartRecommender()


@router.post("/recommendations", response_model=Dict)
async def get_recommendations(request: RecommendationRequest):
    """
    Main endpoint - Returns smart recommendations for user
    
    Algorithm:
    - Analyzes 4 factors: Urgency, Seasonality, Importance, Activity
    - Applies weighted scoring model
    - Ranks services by priority
    - Generates actionable SMS alerts
    
    Developer: Ghadeer - AI/ML Engineer
    """
    try:
        user_dict = request.user.model_dump()
        services_dict = [s.model_dump() for s in request.services]
        
        result = recommender.get_recommendations(
            user_dict,
            services_dict,
            request.top_n
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint - Verify API is running
    """
    return {
        "status": "healthy",
        "service": "Smart Government API",
        "version": "1.0.0",
        "developer": "Ghadeer"
    }


@router.get("/")
async def api_info():
    """
    API Information
    """
    return {
        "message": "Smart Government API - Smart Government Services Recommendations",
        "description": "AI-powered recommendation engine for prioritizing government services",
        "developer": "Ghadeer - AI/ML Engineer",
        "endpoints": {
            "recommendations": {
                "method": "POST",
                "path": "/api/recommendations",
                "description": "Get personalized service recommendations"
            },
            "health": {
                "method": "GET",
                "path": "/api/health",
                "description": "Check API health"
            },
            "docs": {
                "method": "GET",
                "path": "/docs",
                "description": "Interactive API documentation (Swagger UI)"
            }
        },
        "features": [
            "4-factor scoring git --versionalgorithm",
            "Weighted priority calculation",
            "SMS alert generation",
            "Seasonal demand analysis",
            "User behavior patterns"
        ]
    }


@router.get("/weights")
async def get_model_weights():
    """
    Get current model weights
    """
    from app.core.scoring import ServiceScorer
    scorer = ServiceScorer()
    
    return {
        "weights": scorer.WEIGHTS,
        "description": {
            "urgency": "Time sensitivity - How soon does it expire?",
            "seasonality": "Seasonal demand patterns",
            "importance": "Service category criticality",
            "activity": "User engagement level"
        },
        "note": "Weights are tunable based on real usage data"
    }