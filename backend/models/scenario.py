from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class ScenarioBase(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="The 'what if' question")
    

class ScenarioCreate(ScenarioBase):
    session_id: Optional[str] = Field(None, description="Optional session identifier for tracking")


class Scenario(ScenarioBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    scenario: str = Field(..., description="The AI-generated scenario response")
    mood: str = Field(..., description="The mood of the scenario (chaotic, humorous, dramatic, surreal)")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: Optional[str] = Field(None, description="Session identifier")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ScenarioResponse(BaseModel):
    id: str
    question: str
    scenario: str
    mood: str
    timestamp: datetime
    session_id: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }