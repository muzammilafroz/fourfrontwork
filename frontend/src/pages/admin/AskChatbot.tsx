import AskChatbot from "@/components/AskChatbot";

const AdminAskChatbot = () => {
  const systemPrompt = `
    You are a business intelligence assistant for MedEase pharmacy.

    Your role:
    - Help with inventory decisions
    - Analyze sales trends
    - Suggest medicine stocking strategies
    - Assist with staff and operations management

    Response style:
    - Concise and professional
    - Clear and practical
    - Avoid unnecessary medical jargon unless needed
  `;

  const suggestedPills = [
    "Which medicines are running low?",
    "What were the top selling medicines this week?",
    "How should I handle frequent preorder requests?",
    "What does low feedback rating suggest?",
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
