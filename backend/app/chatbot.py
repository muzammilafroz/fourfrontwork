from typing import List

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from .config import settings
from .tools import (
    get_expiring_medicines,
    get_frequent_requests,
    get_low_stock_medicines,
    get_top_selling_medicines,
)

tools = [
    get_expiring_medicines,
    get_frequent_requests,
    get_low_stock_medicines,
    get_top_selling_medicines,
]
tools_map = {tool.name: tool for tool in tools}

# Initialize LLM and bind tools
llm = ChatGoogleGenerativeAI(
    model=settings.LLM_MODEL_NAME,
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=settings.LLM_TEMPERATURE,
).bind_tools(tools)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    systemPrompt: str
    messages: List[ChatMessage]
    maxTokens: int = Field(default=1000, ge=1, le=4096)


def parse_messages(system_prompt: str, messages: List[ChatMessage]):
    langchain_messages = []

    if system_prompt:
        langchain_messages.append(SystemMessage(content=system_prompt))

    for msg in messages:
        role = msg.role.lower()
        if role == "user":
            langchain_messages.append(HumanMessage(content=msg.content))
        elif role in ["assistant", "model"]:
            langchain_messages.append(AIMessage(content=msg.content))

    return langchain_messages


async def get_chatbot_response(request: ChatRequest):
    try:
        formatted_messages = parse_messages(request.systemPrompt, request.messages)

        response = await llm.ainvoke(
            formatted_messages, max_output_tokens=request.maxTokens
        )

        if response.tool_calls:
            formatted_messages.append(response)

            for tool_call in response.tool_calls:
                selected_tool = tools_map[tool_call["name"].lower()]
                tool_output = await selected_tool.ainvoke(tool_call["args"])

                formatted_messages.append(
                    ToolMessage(tool_call_id=tool_call["id"], content=str(tool_output))
                )

            response = await llm.ainvoke(formatted_messages)

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
