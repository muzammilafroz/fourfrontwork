import { useAuthStore } from "@/stores/authStore";

const API = "http://localhost:8000/api/chatbot";

export async function callGemini(
  systemPrompt: string,
  messages: Array<{ role: string; content: any }>,
  maxTokens = 1000,
) {
  const token = useAuthStore.getState().user.auth_token;

  const res = await fetch(API, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      systemPrompt,
      messages,
      maxTokens,
    }),
  });

  if (!res.ok) throw new Error("AI request failed");

  const data = await res.json();
  return data.text;
}

export async function callGeminiVision(
  systemPrompt: string,
  base64Data: string,
  mediaType: string,
  textPrompt: string,
) {
  const token = useAuthStore.getState().user.auth_token;

  const res = await fetch(`${API}/vision`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      systemPrompt,
      base64Data,
      mediaType,
      textPrompt,
    }),
  });

  if (!res.ok) throw new Error("Vision request failed");

  const data = await res.json();
  return data.text;
}
