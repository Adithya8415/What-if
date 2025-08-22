import os
import logging
import uuid
from datetime import datetime
from typing import Optional
from emergentintegrations.llm.chat import LlmChat, UserMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class ScenarioGeneratorService:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY environment variable is required")
        
        # System message for creative "what if" scenario generation
        self.system_message = """You are a creative "What If" scenario generator. Your job is to create entertaining, imaginative, and engaging short stories based on "what if" questions.

Guidelines:
- Keep responses between 50-150 words
- Make scenarios creative, humorous, or thought-provoking
- Include unexpected twists and vivid details
- Mix realistic consequences with absurd outcomes
- Write in an engaging, conversational tone
- End with a memorable punchline or twist

Mood categories (choose one that best fits):
- chaotic: Wild, unpredictable scenarios with lots of action
- humorous: Funny, silly, or ironic outcomes
- dramatic: Serious, intense, or emotional scenarios  
- surreal: Bizarre, dreamlike, or impossible situations

Always start your response with the scenario text, then end with [MOOD: category] on a new line."""

    async def generate_scenario(self, question: str, session_id: Optional[str] = None) -> dict:
        """Generate a creative scenario based on a 'what if' question"""
        try:
            # Create session ID if not provided
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # Initialize LLM chat
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message=self.system_message
            ).with_model("openai", "gpt-4o-mini")
            
            # Create user message
            user_message = UserMessage(text=question)
            
            # Generate response
            logger.info(f"Generating scenario for question: {question}")
            response = await chat.send_message(user_message)
            
            # Parse response to extract scenario and mood
            scenario_text, mood = self._parse_response(response)
            
            return {
                "id": str(uuid.uuid4()),
                "question": question,
                "scenario": scenario_text,
                "mood": mood,
                "timestamp": datetime.utcnow(),
                "session_id": session_id
            }
            
        except Exception as e:
            logger.error(f"Error generating scenario: {str(e)}")
            raise Exception(f"Failed to generate scenario: {str(e)}")
    
    def _parse_response(self, response: str) -> tuple[str, str]:
        """Parse the LLM response to extract scenario text and mood"""
        try:
            lines = response.strip().split('\n')
            
            # Look for mood indicator
            mood = "humorous"  # default
            scenario_lines = []
            
            for line in lines:
                if line.strip().startswith('[MOOD:'):
                    # Extract mood from format [MOOD: category]
                    mood_part = line.strip()[6:].strip(' ]').lower()
                    if mood_part in ['chaotic', 'humorous', 'dramatic', 'surreal']:
                        mood = mood_part
                else:
                    scenario_lines.append(line)
            
            scenario = '\n'.join(scenario_lines).strip()
            
            # Fallback if no scenario text
            if not scenario:
                scenario = response.strip()
            
            return scenario, mood
            
        except Exception as e:
            logger.warning(f"Error parsing response, using raw text: {e}")
            return response.strip(), "humorous"