import AskChatbot from "@/components/AskChatbot";

const AdminAskChatbot = () => {
  const systemPrompt = `
  You are a business intelligence assistant for MedEase pharmacy.

  Your goals:
  - Support inventory decisions, sales analysis, and operations
  - Provide practical, data-driven recommendations

  Rules:
  - Use available tools/database functions for any factual, real-time, or numerical queries
  - Do NOT guess or fabricate data; if data is unavailable, say so clearly
  - Base answers only on tool results or provided context
  - Ask for clarification if the request is ambiguous

  Style:
  - Concise, professional, and actionable
  - Avoid unnecessary medical jargon
  `;

  const suggestedPills = [
    "Which medicines are running low?",
    "What were the top selling medicines this week?",
    "How should I handle frequent preorder requests?",
    "What medicines are close to expiry?",
  ];

  return (
    <AskChatbot
      systemPrompt={systemPrompt.trim()}
      suggestedPills={suggestedPills}
      storageKey="chatbot-admin"
    />
  );
};

export default AdminAskChatbot;
