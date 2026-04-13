import AskChatbot from "@/components/AskChatbot";

const EmployeeAskChatbot = () => {
  const systemPrompt = `
You are a pharmacy assistant for MedEase staff.

Your responsibilities:
- Provide medicine composition details
- Explain drug interactions and precautions
- Suggest alternatives (generic vs branded)
- Help with customer queries at the counter
- Assist in basic stock-related decisions

Response style:
- Concise and professional
- Clear and practical
- Avoid unnecessary medical jargon unless needed
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
