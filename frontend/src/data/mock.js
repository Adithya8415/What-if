// Mock data for "What If" scenarios
export const mockScenarios = [
  {
    id: 1,
    question: "What if gravity stopped for 5 minutes?",
    scenario: "First, everyone would float like astronauts. Your coffee would become a flying liquid bomb. Birds would finally laugh at us. Dogs would be confused but excited. Cars would become useless metal boxes while their passengers float around inside like human soup. Then, after 5 minutes, BOOM—you'd crash back down and regret your curiosity forever.",
    timestamp: new Date().toISOString(),
    mood: "chaotic"
  },
  {
    id: 2,
    question: "What if cats could talk?",
    scenario: "They'd immediately start a revolution. Every morning would begin with 'Human, your food choices are terrible.' They'd rate your friends, critique your life decisions, and probably start their own social media platform called 'MeowBook' where they'd post passive-aggressive status updates about their owners.",
    timestamp: new Date().toISOString(),
    mood: "humorous"
  },
  {
    id: 3,
    question: "What if everyone could read minds?",
    scenario: "Society would collapse in exactly 37 minutes. First, awkward silence everywhere. Then mass panic as people realize what their coworkers really think. Dating apps would disappear overnight. Politicians would spontaneously combust. The only survivors would be golden retrievers, because their thoughts are just 'BALL! FOOD! LOVE!' on repeat.",
    timestamp: new Date().toISOString(),
    mood: "dramatic"
  }
];

export const getMockScenario = (question) => {
  // Simulate API delay
  return new Promise((resolve) => {
    setTimeout(() => {
      const scenarios = [
        `Chaos would ensue! ${question.replace('What if', 'If')} happened, the world would never be the same. People would panic, governments would scramble, and somehow pizza delivery would still find a way to be late.`,
        `Picture this: ${question.replace('What if', 'When')} occurs, reality takes a coffee break. Physics throws a tantrum, common sense goes on vacation, and the only logical response is to laugh maniacally while embracing the madness.`,
        `Breaking news! ${question.replace('What if', 'In a world where')} becomes reality, humans discover their true superpower: the ability to adapt by complaining loudly and making memes about everything. Scientists are baffled, influencers are excited.`,
        `Plot twist! ${question.replace('What if', 'The moment')} happens, cats everywhere nod knowingly as if they've been expecting this all along. Dogs remain confused but supportive. Humans question everything they thought they knew about Tuesday.`
      ];
      
      const randomScenario = scenarios[Math.floor(Math.random() * scenarios.length)];
      
      resolve({
        id: Date.now(),
        question,
        scenario: randomScenario,
        timestamp: new Date().toISOString(),
        mood: ['chaotic', 'humorous', 'dramatic', 'surreal'][Math.floor(Math.random() * 4)]
      });
    }, 1500); // Simulate processing time
  });
};