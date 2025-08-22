import React from 'react';
import { Brain, Zap } from 'lucide-react';

const Header = () => {
  return (
    <header className="w-full py-8 px-4">
      <div className="max-w-4xl mx-auto text-center">
        {/* Logo and Title */}
        <div className="flex items-center justify-center gap-3 mb-4">
          <div className="relative">
            <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-pink-500 rounded-xl flex items-center justify-center shadow-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div className="absolute -top-1 -right-1 w-4 h-4 bg-yellow-400 rounded-full flex items-center justify-center">
              <Zap className="w-2.5 h-2.5 text-yellow-800" />
            </div>
          </div>
          <div>
            <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-orange-600 to-pink-600 bg-clip-text text-transparent">
              What If?
            </h1>
            <p className="text-sm text-gray-500 font-medium">Scenario Generator</p>
          </div>
        </div>

        {/* Subtitle */}
        <p className="text-lg md:text-xl text-gray-600 mb-2 font-medium">
          Explore endless possibilities with AI-powered scenarios
        </p>
        <p className="text-sm text-gray-500 max-w-md mx-auto leading-relaxed">
          Ask any "what if" question and watch as creative, entertaining scenarios unfold before your eyes
        </p>

        {/* Decorative Elements */}
        <div className="flex justify-center gap-8 mt-6 opacity-60">
          <div className="w-2 h-2 bg-orange-300 rounded-full animate-pulse"></div>
          <div className="w-2 h-2 bg-pink-300 rounded-full animate-pulse delay-75"></div>
          <div className="w-2 h-2 bg-yellow-300 rounded-full animate-pulse delay-150"></div>
        </div>
      </div>
    </header>
  );
};

export default Header;