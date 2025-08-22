# Backend Development Contracts - What If Scenario Generator

## API Contracts

### 1. Generate Scenario Endpoint
**POST /api/scenarios/generate**
```json
Request:
{
  "question": "What if gravity stopped for 5 minutes?",
  "session_id": "optional-session-identifier"
}

Response:
{
  "id": "generated-uuid",
  "question": "What if gravity stopped for 5 minutes?",
  "scenario": "AI-generated scenario text...",
  "mood": "chaotic|humorous|dramatic|surreal",
  "timestamp": "2025-07-22T10:30:00.000Z",
  "session_id": "session-identifier"
}
```

### 2. Get User's Scenario History
**GET /api/scenarios/history?session_id=xxx&limit=10**
```json
Response:
{
  "scenarios": [
    {
      "id": "uuid",
      "question": "question text",
      "scenario": "scenario text",
      "mood": "mood",
      "timestamp": "timestamp",
      "session_id": "session_id"
    }
  ],
  "total": 25,
  "page": 1,
  "limit": 10
}
```

## Mock Data to Replace

### Frontend Mock Functions
- `getMockScenario()` in `/app/frontend/src/data/mock.js` will be replaced with actual API call
- Remove mock delay and scenarios array
- Replace with axios call to `/api/scenarios/generate`

### Mock Data Elements
- Predefined scenario responses
- Simulated processing delay (1.5s)
- Random mood assignment
- Static scenario generation

## Backend Implementation Plan

### 1. Database Models
```javascript
// Scenario Model
{
  id: String (UUID),
  question: String (required),
  scenario: String (required),
  mood: String (enum: chaotic, humorous, dramatic, surreal),
  timestamp: Date,
  session_id: String (for user tracking),
  created_at: Date,
  updated_at: Date
}

// Optional: User Session Model
{
  session_id: String (UUID),
  created_at: Date,
  last_activity: Date,
  scenario_count: Number
}
```

### 2. LLM Integration
- Install `emergentintegrations` library
- Use EMERGENT_LLM_KEY for AI scenario generation
- Default model: `gpt-4o-mini` by OpenAI
- Custom system prompt for creative "what if" scenarios
- Mood detection from AI response

### 3. API Endpoints Implementation
- POST `/api/scenarios/generate` - Main scenario generation
- GET `/api/scenarios/history` - User's scenario history
- Error handling for LLM failures
- Input validation and sanitization

## Frontend & Backend Integration

### 1. Replace Mock Function
**From:** `getMockScenario(question)` in mock.js  
**To:** API call `POST /api/scenarios/generate`

### 2. Session Management
- Generate session_id in frontend (localStorage)
- Send session_id with each request
- Enable scenario history feature later

### 3. Error Handling
- Network errors
- LLM API failures
- Rate limiting
- Input validation errors

### 4. Loading States
- Keep existing loading UI
- Add error states for failed generations
- Add retry functionality

## Implementation Steps

1. **Install Dependencies**
   - `emergentintegrations` library
   - Add EMERGENT_LLM_KEY to backend/.env

2. **Create Database Models**
   - Scenario model with MongoDB

3. **Implement LLM Service**
   - Scenario generation service
   - Mood detection logic
   - Error handling

4. **Create API Endpoints**
   - Generate scenario endpoint
   - History endpoint (optional for MVP)

5. **Update Frontend**
   - Replace mock.js with API calls
   - Update error handling
   - Test full integration

6. **Testing**
   - Backend API testing
   - Frontend integration testing
   - End-to-end scenario generation