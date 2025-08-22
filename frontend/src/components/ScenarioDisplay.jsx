import React from 'react';
import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Copy, Share2, RotateCcw, Clock } from 'lucide-react';
import { useToast } from '../hooks/use-toast';

const ScenarioDisplay = ({ scenario, onNewScenario }) => {
  const { toast } = useToast();

  if (!scenario) return null;

  const handleCopy = () => {
    const text = `Q: ${scenario.question}\n\nA: ${scenario.scenario}`;
    navigator.clipboard.writeText(text).then(() => {
      toast({
        title: "Copied to clipboard!",
        description: "Scenario copied successfully",
      });
    });
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: 'What If Scenario',
        text: `${scenario.question}\n\n${scenario.scenario}`,
      });
    } else {
      handleCopy();
    }
  };

  const getMoodColor = (mood) => {
    const colors = {
      chaotic: 'bg-red-100 text-red-700 border-red-200',
      humorous: 'bg-yellow-100 text-yellow-700 border-yellow-200',
      dramatic: 'bg-purple-100 text-purple-700 border-purple-200',
      surreal: 'bg-blue-100 text-blue-700 border-blue-200'
    };
    return colors[mood] || 'bg-gray-100 text-gray-700 border-gray-200';
  };

  const getMoodEmoji = (mood) => {
    const emojis = {
      chaotic: '💥',
      humorous: '😄',
      dramatic: '🎭',
      surreal: '🌀'
    };
    return emojis[mood] || '✨';
  };

  return (
    <div className="w-full max-w-2xl mx-auto px-4 animate-in slide-in-from-bottom-4 duration-500">
      <Card className="p-6 bg-gradient-to-br from-white to-orange-50 border-orange-200 shadow-xl">
        {/* Question Header */}
        <div className="mb-6">
          <div className="flex items-start gap-3 mb-3">
            <div className="text-2xl">{getMoodEmoji(scenario.mood)}</div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-gray-800 leading-tight">
                {scenario.question}
              </h3>
              <div className="flex items-center gap-2 mt-2">
                <div className={`px-2 py-1 rounded-full text-xs border ${getMoodColor(scenario.mood)} capitalize`}>
                  {scenario.mood}
                </div>
                <div className="flex items-center gap-1 text-xs text-gray-500">
                  <Clock className="w-3 h-3" />
                  {new Date(scenario.timestamp).toLocaleTimeString([], { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Scenario Content */}
        <div className="mb-6">
          <div className="bg-white rounded-lg p-4 border border-orange-100 shadow-sm">
            <p className="text-gray-700 leading-relaxed text-base">
              {scenario.scenario}
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-3 justify-between items-center">
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleCopy}
              className="text-gray-600 hover:text-orange-600 hover:border-orange-300 hover:bg-orange-50 transition-all duration-200"
            >
              <Copy className="w-4 h-4 mr-1" />
              Copy
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleShare}
              className="text-gray-600 hover:text-orange-600 hover:border-orange-300 hover:bg-orange-50 transition-all duration-200"
            >
              <Share2 className="w-4 h-4 mr-1" />
              Share
            </Button>
          </div>
          
          <Button
            onClick={onNewScenario}
            className="bg-gradient-to-r from-orange-500 to-pink-500 hover:from-orange-600 hover:to-pink-600 text-white font-semibold px-4 py-2 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 transform hover:scale-105"
          >
            <RotateCcw className="w-4 h-4 mr-2" />
            Ask Another
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default ScenarioDisplay;