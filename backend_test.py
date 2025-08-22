#!/usr/bin/env python3
"""
Backend API Tests for What If Scenario Generator
Tests all backend endpoints and functionality
"""

import asyncio
import aiohttp
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://wonder-machine.preview.emergentagent.com')
API_BASE_URL = f"{BACKEND_URL}/api"

class BackendTester:
    def __init__(self):
        self.session = None
        self.test_results = []
        self.session_id = str(uuid.uuid4())
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        if response_data:
            result['response_data'] = response_data
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success and response_data:
            print(f"   Response: {response_data}")
        print()
    
    async def test_health_check(self):
        """Test GET /api/ endpoint"""
        try:
            async with self.session.get(f"{API_BASE_URL}/") as response:
                if response.status == 200:
                    data = await response.json()
                    if "message" in data and "running" in data["message"].lower():
                        self.log_test("Health Check", True, f"API is running: {data['message']}")
                        return True
                    else:
                        self.log_test("Health Check", False, f"Unexpected response format", data)
                        return False
                else:
                    text = await response.text()
                    self.log_test("Health Check", False, f"HTTP {response.status}", text)
                    return False
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    async def test_scenario_generation_basic(self):
        """Test basic scenario generation"""
        test_question = "What if cats ruled the world?"
        payload = {
            "question": test_question,
            "session_id": self.session_id
        }
        
        try:
            async with self.session.post(
                f"{API_BASE_URL}/scenarios/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    
                    # Validate response structure
                    required_fields = ['id', 'question', 'scenario', 'mood', 'timestamp', 'session_id']
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        self.log_test("Basic Scenario Generation", False, 
                                    f"Missing fields: {missing_fields}", data)
                        return False
                    
                    # Validate field values
                    if data['question'] != test_question:
                        self.log_test("Basic Scenario Generation", False, 
                                    f"Question mismatch: expected '{test_question}', got '{data['question']}'")
                        return False
                    
                    if data['session_id'] != self.session_id:
                        self.log_test("Basic Scenario Generation", False, 
                                    f"Session ID mismatch: expected '{self.session_id}', got '{data['session_id']}'")
                        return False
                    
                    # Validate mood is one of expected values
                    valid_moods = ['chaotic', 'humorous', 'dramatic', 'surreal']
                    if data['mood'] not in valid_moods:
                        self.log_test("Basic Scenario Generation", False, 
                                    f"Invalid mood: '{data['mood']}', expected one of {valid_moods}")
                        return False
                    
                    # Validate scenario content exists and is reasonable length
                    if not data['scenario'] or len(data['scenario']) < 10:
                        self.log_test("Basic Scenario Generation", False, 
                                    f"Scenario too short or empty: '{data['scenario']}'")
                        return False
                    
                    self.log_test("Basic Scenario Generation", True, 
                                f"Generated scenario with mood '{data['mood']}', length {len(data['scenario'])} chars")
                    return True
                    
                else:
                    text = await response.text()
                    self.log_test("Basic Scenario Generation", False, 
                                f"HTTP {response.status}", text)
                    return False
                    
        except Exception as e:
            self.log_test("Basic Scenario Generation", False, f"Error: {str(e)}")
            return False
    
    async def test_scenario_generation_different_types(self):
        """Test scenario generation with different types of questions"""
        test_cases = [
            ("What if gravity stopped working?", "serious/scientific"),
            ("What if dogs could talk but only complained about everything?", "silly/humorous"),
            ("What if every time you sneezed, you teleported to a random location?", "crazy/surreal"),
            ("What if money grew on trees but only during full moons?", "whimsical")
        ]
        
        success_count = 0
        
        for question, question_type in test_cases:
            payload = {
                "question": question,
                "session_id": self.session_id
            }
            
            try:
                async with self.session.post(
                    f"{API_BASE_URL}/scenarios/generate",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Basic validation
                        if all(field in data for field in ['id', 'question', 'scenario', 'mood']):
                            if len(data['scenario']) > 10:
                                success_count += 1
                                print(f"   ✅ {question_type}: Generated {len(data['scenario'])} chars, mood: {data['mood']}")
                            else:
                                print(f"   ❌ {question_type}: Scenario too short")
                        else:
                            print(f"   ❌ {question_type}: Missing required fields")
                    else:
                        print(f"   ❌ {question_type}: HTTP {response.status}")
                        
            except Exception as e:
                print(f"   ❌ {question_type}: Error - {str(e)}")
        
        success = success_count == len(test_cases)
        self.log_test("Different Question Types", success, 
                    f"Successfully generated scenarios for {success_count}/{len(test_cases)} question types")
        return success
    
    async def test_scenario_history_empty(self):
        """Test scenario history when no scenarios exist for a new session"""
        new_session_id = str(uuid.uuid4())
        
        try:
            async with self.session.get(
                f"{API_BASE_URL}/scenarios/history?session_id={new_session_id}"
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    
                    if isinstance(data, list) and len(data) == 0:
                        self.log_test("Empty History", True, "Correctly returned empty list for new session")
                        return True
                    else:
                        self.log_test("Empty History", False, 
                                    f"Expected empty list, got: {data}")
                        return False
                else:
                    text = await response.text()
                    self.log_test("Empty History", False, f"HTTP {response.status}", text)
                    return False
                    
        except Exception as e:
            self.log_test("Empty History", False, f"Error: {str(e)}")
            return False
    
    async def test_scenario_history_with_data(self):
        """Test scenario history retrieval after generating scenarios"""
        # First generate a few scenarios
        questions = [
            "What if pizza could fly?",
            "What if books read themselves to you?",
            "What if mirrors showed your future instead of your reflection?"
        ]
        
        generated_ids = []
        
        for question in questions:
            payload = {
                "question": question,
                "session_id": self.session_id
            }
            
            try:
                async with self.session.post(
                    f"{API_BASE_URL}/scenarios/generate",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        generated_ids.append(data['id'])
                    else:
                        print(f"   Failed to generate scenario for: {question}")
                        
            except Exception as e:
                print(f"   Error generating scenario: {e}")
        
        # Now test history retrieval
        try:
            async with self.session.get(
                f"{API_BASE_URL}/scenarios/history?session_id={self.session_id}"
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    
                    if isinstance(data, list):
                        # Should have at least the scenarios we just generated
                        if len(data) >= len(generated_ids):
                            # Validate structure of returned scenarios
                            valid_scenarios = 0
                            for scenario in data:
                                required_fields = ['id', 'question', 'scenario', 'mood', 'timestamp']
                                if all(field in scenario for field in required_fields):
                                    if scenario['session_id'] == self.session_id:
                                        valid_scenarios += 1
                            
                            if valid_scenarios >= len(generated_ids):
                                self.log_test("History with Data", True, 
                                            f"Retrieved {len(data)} scenarios, {valid_scenarios} valid for session")
                                return True
                            else:
                                self.log_test("History with Data", False, 
                                            f"Only {valid_scenarios} valid scenarios out of {len(data)}")
                                return False
                        else:
                            self.log_test("History with Data", False, 
                                        f"Expected at least {len(generated_ids)} scenarios, got {len(data)}")
                            return False
                    else:
                        self.log_test("History with Data", False, 
                                    f"Expected list, got: {type(data)}")
                        return False
                else:
                    text = await response.text()
                    self.log_test("History with Data", False, f"HTTP {response.status}", text)
                    return False
                    
        except Exception as e:
            self.log_test("History with Data", False, f"Error: {str(e)}")
            return False
    
    async def test_scenario_history_pagination(self):
        """Test scenario history pagination parameters"""
        try:
            # Test with limit parameter
            async with self.session.get(
                f"{API_BASE_URL}/scenarios/history?limit=2"
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    
                    if isinstance(data, list) and len(data) <= 2:
                        self.log_test("History Pagination", True, 
                                    f"Limit parameter working, returned {len(data)} scenarios")
                        return True
                    else:
                        self.log_test("History Pagination", False, 
                                    f"Limit not respected, returned {len(data)} scenarios")
                        return False
                else:
                    text = await response.text()
                    self.log_test("History Pagination", False, f"HTTP {response.status}", text)
                    return False
                    
        except Exception as e:
            self.log_test("History Pagination", False, f"Error: {str(e)}")
            return False
    
    async def test_error_handling_invalid_input(self):
        """Test error handling for invalid inputs"""
        test_cases = [
            ({}, "empty payload"),
            ({"question": ""}, "empty question"),
            ({"question": "x" * 1000}, "question too long"),
            ({"invalid_field": "test"}, "missing question field")
        ]
        
        success_count = 0
        
        for payload, description in test_cases:
            try:
                async with self.session.post(
                    f"{API_BASE_URL}/scenarios/generate",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    # Should return 4xx error for invalid input
                    if 400 <= response.status < 500:
                        success_count += 1
                        print(f"   ✅ {description}: Correctly returned HTTP {response.status}")
                    else:
                        print(f"   ❌ {description}: Expected 4xx error, got HTTP {response.status}")
                        
            except Exception as e:
                print(f"   ❌ {description}: Unexpected error - {str(e)}")
        
        success = success_count == len(test_cases)
        self.log_test("Error Handling", success, 
                    f"Correctly handled {success_count}/{len(test_cases)} invalid inputs")
        return success
    
    async def test_database_persistence(self):
        """Test that scenarios are properly saved to database"""
        # Generate a unique scenario
        unique_question = f"What if test scenario {uuid.uuid4().hex[:8]}?"
        test_session_id = str(uuid.uuid4())
        
        payload = {
            "question": unique_question,
            "session_id": test_session_id
        }
        
        try:
            # Generate scenario
            async with self.session.post(
                f"{API_BASE_URL}/scenarios/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status != 200:
                    self.log_test("Database Persistence", False, "Failed to generate test scenario")
                    return False
                
                generated_data = await response.json()
                generated_id = generated_data['id']
            
            # Wait a moment for database write
            await asyncio.sleep(1)
            
            # Retrieve from history
            async with self.session.get(
                f"{API_BASE_URL}/scenarios/history?session_id={test_session_id}"
            ) as response:
                
                if response.status == 200:
                    history_data = await response.json()
                    
                    # Find our scenario in the history
                    found_scenario = None
                    for scenario in history_data:
                        if scenario['id'] == generated_id:
                            found_scenario = scenario
                            break
                    
                    if found_scenario:
                        # Verify data integrity
                        if (found_scenario['question'] == unique_question and
                            found_scenario['session_id'] == test_session_id and
                            found_scenario['scenario'] == generated_data['scenario']):
                            
                            self.log_test("Database Persistence", True, 
                                        "Scenario correctly saved and retrieved from database")
                            return True
                        else:
                            self.log_test("Database Persistence", False, 
                                        "Data mismatch between generated and retrieved scenario")
                            return False
                    else:
                        self.log_test("Database Persistence", False, 
                                    f"Generated scenario with ID {generated_id} not found in history")
                        return False
                else:
                    text = await response.text()
                    self.log_test("Database Persistence", False, 
                                f"Failed to retrieve history: HTTP {response.status}")
                    return False
                    
        except Exception as e:
            self.log_test("Database Persistence", False, f"Error: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """Run all backend tests"""
        print(f"🚀 Starting Backend API Tests")
        print(f"Backend URL: {API_BASE_URL}")
        print(f"Test Session ID: {self.session_id}")
        print("=" * 60)
        
        tests = [
            self.test_health_check,
            self.test_scenario_generation_basic,
            self.test_scenario_generation_different_types,
            self.test_scenario_history_empty,
            self.test_scenario_history_with_data,
            self.test_scenario_history_pagination,
            self.test_error_handling_invalid_input,
            self.test_database_persistence
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                result = await test()
                if result:
                    passed += 1
            except Exception as e:
                print(f"❌ {test.__name__} - Unexpected error: {str(e)}")
        
        print("=" * 60)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Backend API is working correctly.")
        else:
            print(f"⚠️  {total - passed} tests failed. Check the details above.")
        
        return passed, total, self.test_results


async def main():
    """Main test runner"""
    async with BackendTester() as tester:
        passed, total, results = await tester.run_all_tests()
        
        # Save detailed results
        with open('/app/backend_test_results.json', 'w') as f:
            json.dump({
                'summary': {
                    'passed': passed,
                    'total': total,
                    'success_rate': passed / total if total > 0 else 0
                },
                'results': results,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        
        return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)