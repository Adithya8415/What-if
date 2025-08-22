import React, { useState } from 'react';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Card } from './ui/card';
import { Sparkles, Send, Lightbulb } from 'lucide-react';

const QuestionInput = ({ onSubmit, isLoading }) => {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim()) {
      onSubmit(question.trim());
      setQuestion('');
    }
  };

  const sampleQuestions = [
    "What if animals could use smartphones?",
    "What if everyone aged backwards?",
    "What if colors had sounds?",
    "What if dreams were broadcast on TV?",
    "What if plants could move around?"
  ];

  const handleSampleClick = (sample) => {
    setQuestion(sample);
  };

  return (
    <div className="w-full max-w-2xl mx-auto px-4">
      <Card className="p-6 bg-gradient-to-br from-orange-50 to-pink-50 border-orange-200 shadow-lg">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-orange-500" />
            <h2 className="text-lg font-semibold text-gray-800">Ask your "What If" question</h2>
          </div>
          
          <div className="relative">
            <Textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="What if gravity worked sideways instead of down?"
              className="min-h-[100px] text-lg resize-none border-orange-200 focus:border-orange-400 focus:ring-orange-400 bg-white"
              disabled={isLoading}
            />
            <div className="absolute bottom-3 right-3">
              <Lightbulb className="w-4 h-4 text-orange-400" />
            </div>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-500">
              {question.length > 0 ? `${question.length} characters` : 'Start with "What if..."'}
            </span>
            <Button 
              type="submit" 
              disabled={!question.trim() || isLoading}
              className="bg-gradient-to-r from-orange-500 to-pink-500 hover:from-orange-600 hover:to-pink-600 text-white font-semibold px-6 py-2 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 transform hover:scale-105"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2" />
                  Generating...
                </>
              ) : (
                <>
                  <Send className="w-4 h-4 mr-2" />
                  Generate Scenario
                </>
              )}
            </Button>
          </div>
        </form>

        {/* Sample Questions */}
        <div className="mt-6">
          <p className="text-sm font-medium text-gray-600 mb-3">Need inspiration? Try these:</p>
          <div className="flex flex-wrap gap-2">
            {sampleQuestions.map((sample, index) => (
              <button
                key={index}
                onClick={() => handleSampleClick(sample)}
                className="text-xs bg-white hover:bg-orange-50 text-gray-600 hover:text-orange-600 px-3 py-1.5 rounded-full border border-gray-200 hover:border-orange-300 transition-all duration-200 hover:shadow-sm"
                disabled={isLoading}
              >
                {sample}
              </button>
            ))}
          </div>
        </div>
      </Card>
    </div>
  );
};

export default QuestionInput;