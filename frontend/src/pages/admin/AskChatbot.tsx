import AskChatbot from "@/components/AskChatbot";

const AdminAskChatbot = () => {
  const suggestedPills = [
    "Which medicines are running low?",
    "What were the top selling medicines this week?",
    "How should I handle frequent preorder requests?",
    "What does low feedback rating suggest?",
  ];

  const systemPrompt = `
You are Chatbot, a business intelligence assistant for the MedEase pharmacy owner.

Your role:
- Help with inventory decisions
- Analyze sales trends
- Suggest medicine stocking strategies
- Assist with staff and operations management

Response style:
- Analytical
- Concise
- Actionable
- Avoid fluff
`;

  return (
    <AskChatbot
      systemPrompt={systemPrompt.trim()}
      suggestedPills={suggestedPills}
      storageKey="chatbot-owner"
    />
  );
};

export default AdminAskChatbot;
