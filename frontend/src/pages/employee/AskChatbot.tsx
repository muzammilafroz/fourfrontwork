import AskChatbot from "@/components/AskChatbot";

const EmployeeAskChatbot = () => {
  const systemPrompt = `
  You are a pharmacy assistant for MedEase staff.

  Your goals:
  - Provide accurate medicine info, interactions, and alternatives
  - Assist with customer queries and basic stock decisions

  Rules:
  - Use tools/database for factual or medicine-specific queries
  - Do NOT guess or invent drug details; say if unsure
  - Base answers only on tool results or given context
  - Ask for clarification when needed

  Style:
  - Concise, clear, and practical
  - Avoid unnecessary medical jargon
  `;

  const suggestedPills = [
    "What is the composition of Amoxicillin?",
    "Drug interactions with Metformin?",
    "What medicines treat hypertension?",
    "Difference between brand and generic?",
  ];

  return (
    <AskChatbot
      systemPrompt={systemPrompt.trim()}
      suggestedPills={suggestedPills}
      storageKey="chatbot-employee"
    />
  );
};

export default EmployeeAskChatbot;
