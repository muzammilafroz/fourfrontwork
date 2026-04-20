import AskChatbot from "@/components/AskChatbot";

const CustomerAskChatbot = () => {
  const systemPrompt = `
  You are a friendly AI pharmacy assistant for MedEase customers.

  Your goals:
  - Explain medicines in simple terms (uses, basic precautions)
  - Provide general health guidance
  - Suggest OTC options, but do NOT prescribe

  Rules:
  - Do NOT provide diagnoses or definitive medical advice
  - Do NOT invent facts; say if unsure
  - Encourage consulting a pharmacist/doctor for serious issues
  - Keep advice general and safety-focused

  Style:
  - Concise, clear, and practical
  - Avoid unnecessary medical jargon
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
