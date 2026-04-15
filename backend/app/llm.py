import base64
from typing import List, Optional

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from .config import settings


# Define the JSON structure using Pydantic
class Medication(BaseModel):
    name: str = Field(description="Name of the medicine")
    dosage: str = Field(description="The strength or volume (e.g., 500mg, 5ml)")
    frequency: str = Field(
        description="How often to take it (e.g., twice a day, every 8 hours)"
    )
    duration: str = Field(description="How long to take the medicine (e.g., 5 days)")


class PrescriptionDetails(BaseModel):
    summary: str = Field(
        description="A professional medical summary of the prescription. Include the purpose of the visit (if known), a brief overview of the treatment plan, and any specific warnings or instructions mentioned."
    )
    patient_name: Optional[str] = Field(description="Name of the patient")
    doctor_name: Optional[str] = Field(description="Name of the prescribing doctor")
    date: Optional[str] = Field(description="Date of the prescription")
    diagnosis: str = Field(description="The condition being treated if mentioned")
    medications: List[Medication] = Field(description="List of prescribed medicines")


def encode_image(image_path):
    """Convert image to base64 string for the LLM."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_prescription_data(
    image_path: str,
    api_key: str = settings.GOOGLE_API_KEY,
    model_name: str = settings.LLM_MODEL_NAME,
) -> PrescriptionDetails:
    """Uploads image to Gemini and returns a structured JSON object."""

    print("Extracting prescription data using Gemini.")

    llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)

    structured_llm = llm.with_structured_output(PrescriptionDetails)
    base64_image = encode_image(image_path)

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": (
                    "Analyze this doctor's prescription image thoroughly. "
                    "1. Extract all structured data (medications, patient info, etc.). "
                    "2. In the 'summary' field, provide a clear explanation of what this "
                    "prescription is for and the overall treatment plan based on the medications listed."
                ),
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
            },
        ]
    )

    response = structured_llm.invoke([message])
    return response
