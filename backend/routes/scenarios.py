from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
import logging
from datetime import datetime

try:
    from ..models.scenario import ScenarioCreate, ScenarioResponse
    from ..services.scenario_service import ScenarioGeneratorService
    from ..database import get_database
except ImportError:
    # Fallback for when running as script
    from models.scenario import ScenarioCreate, ScenarioResponse
    from services.scenario_service import ScenarioGeneratorService
    from database import get_database

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/scenarios", tags=["scenarios"])

# Initialize scenario service
scenario_service = ScenarioGeneratorService()


@router.post("/generate", response_model=ScenarioResponse)
async def generate_scenario(
    request: ScenarioCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Generate a new 'what if' scenario using AI"""
    try:
        # Generate scenario using AI
        scenario_data = await scenario_service.generate_scenario(
            question=request.question,
            session_id=request.session_id
        )
        
        # Save to database
        result = await db.scenarios.insert_one(scenario_data)
        scenario_data["_id"] = str(result.inserted_id)
        
        logger.info(f"Generated scenario with ID: {scenario_data['id']}")
        
        return ScenarioResponse(**scenario_data)
        
    except Exception as e:
        logger.error(f"Error in generate_scenario: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate scenario: {str(e)}"
        )


@router.get("/history", response_model=List[ScenarioResponse])
async def get_scenario_history(
    session_id: Optional[str] = None,
    limit: int = 10,
    skip: int = 0,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get scenario history for a session or all scenarios"""
    try:
        # Build query
        query = {}
        if session_id:
            query["session_id"] = session_id
        
        # Get scenarios with pagination
        cursor = db.scenarios.find(query).sort("timestamp", -1).skip(skip).limit(limit)
        scenarios = await cursor.to_list(length=limit)
        
        # Convert to response format
        scenario_responses = []
        for scenario in scenarios:
            scenario_responses.append(ScenarioResponse(**scenario))
        
        logger.info(f"Retrieved {len(scenario_responses)} scenarios")
        return scenario_responses
        
    except Exception as e:
        logger.error(f"Error in get_scenario_history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve scenario history: {str(e)}"
        )