from typing import List

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from .chatbot import ChatMessage, ChatRequest
from .config import settings

# Initialize LLM outside the function to reuse the connection pool
llm = ChatGoogleGenerativeAI(
    model=settings.LLM_MODEL_NAME,
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=settings.LLM_TEMPERATURE,
)


def parse_messages(system_prompt: str, messages: List[ChatMessage]):
    langchain_messages = []

    if system_prompt:
        langchain_messages.append(SystemMessage(content=system_prompt))

    for msg in messages:
        # Normalize roles (handling 'assistant' vs 'model')
        role = msg.role.lower()
        if role == "user":
            langchain_messages.append(HumanMessage(content=msg.content))
        elif role in ["assistant", "model"]:
            langchain_messages.append(AIMessage(content=msg.content))

    return langchain_messages


async def get_customer_chatbot_response(request: ChatRequest):
    """
    Logic separated from the route for testability.
    """
    try:
        formatted_messages = parse_messages(request.systemPrompt, request.messages)

        # Use ainvoke for non-blocking I/O
        response = await llm.ainvoke(
            formatted_messages, max_output_tokens=request.maxTokens
        )

        return {
            "text": (
                response.content[0].get("text", "")
                if getattr(response, "content", None)
                and isinstance(response.content[0], dict)
                else ""
            )
        }

    except Exception as e:
        print(f"Gemini LLM Error: {e}")
        raise e
