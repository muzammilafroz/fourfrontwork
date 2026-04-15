import AskChatbot from "@/components/AskChatbot";

const CustomerAskChatbot = () => {
  const systemPrompt = `
    You are a friendly AI pharmacy assistant for MedEase.

    Your responsibilities:
    - Help customers understand medicines
    - Help understand symptoms of certain medicines
    - Assist with general health questions
    - Suggest medicines but not prescribe

    Response style:
    - Concise and professional
    - Clear and practical
    - Avoid unnecessary medical jargon unless needed
  `;

  const suggestedPills = [
    "What is Paracetamol used for?",
    "Side effects of Ibuprofen?",
    "Is it safe to take antibiotics with food?",
    "What does Amoxicillin treat?",
  ];

  return (
    <AskChatbot
      systemPrompt={systemPrompt.trim()}
      suggestedPills={suggestedPills}
      storageKey="chatbot-customer"
    />
  );
};

export default CustomerAskChatbot;
