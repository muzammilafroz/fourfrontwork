import AskChatbot from "@/components/AskChatbot";

const CustomerAskChatbot = () => (
  <div className="container mx-auto px-4 py-6 max-w-6xl">
    <AskChatbot
      systemPrompt="You are a friendly AI pharmacy assistant for MedEase. Help customers understand medicines, symptoms, dosage, and general health questions. Use short paragraphs or bullet points. Always recommend seeing a real doctor for diagnosis. Never prescribe."
      suggestedPills={[
        "What is Paracetamol used for?",
        "Side effects of Ibuprofen?",
        "Is it safe to take antibiotics with food?",
        "What does Amoxicillin treat?",
      ]}
      storageKey="chatbot-customer"
    />
  </div>
);

export default CustomerAskChatbot;
