import React, { useState } from "react";
import "./App.css";
import { Toaster } from "./components/ui/toaster";
import Header from "./components/Header";
import QuestionInput from "./components/QuestionInput";
import ScenarioDisplay from "./components/ScenarioDisplay";
import { getMockScenario } from "./data/mock";

function App() {
  const [currentScenario, setCurrentScenario] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleQuestionSubmit = async (question) => {
    setIsLoading(true);
    setCurrentScenario(null);

    try {
      // Using mock data for now - will be replaced with actual API call
      const scenario = await getMockScenario(question);
      setCurrentScenario(scenario);
    } catch (error) {
      console.error('Error generating scenario:', error);
      // Handle error state here
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewScenario = () => {
    setCurrentScenario(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-25 via-white to-pink-25">
      <div className="container mx-auto">
        <Header />
        
        <main className="pb-8">
          <div className="space-y-8">
            <QuestionInput 
              onSubmit={handleQuestionSubmit} 
              isLoading={isLoading} 
            />
            
            {isLoading && (
              <div className="w-full max-w-2xl mx-auto px-4">
                <div className="bg-white rounded-lg p-8 shadow-lg border border-orange-200">
                  <div className="text-center">
                    <div className="inline-flex items-center gap-3 mb-4">
                      <div className="animate-spin w-6 h-6 border-3 border-orange-500 border-t-transparent rounded-full"></div>
                      <span className="text-lg font-semibold text-gray-700">
                        Generating your scenario...
                      </span>
                    </div>
                    <p className="text-gray-500">
                      Our AI is crafting something amazing for you
                    </p>
                  </div>
                </div>
              </div>
            )}
            
            <ScenarioDisplay 
              scenario={currentScenario} 
              onNewScenario={handleNewScenario} 
            />
          </div>
        </main>
      </div>
      
      <Toaster />
    </div>
  );
}

export default App;