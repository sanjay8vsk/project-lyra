from fastapi import APIRouter # type: ignore
from pydantic import BaseModel # type: ignore
from openai import OpenAI # type: ignore
from dotenv import load_dotenv # type: ignore
import os

import app.routes.upload as upload_module

load_dotenv()

router = APIRouter()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat(request: ChatRequest):

    try:

        document_context = upload_module.DOCUMENT_TEXT

        completion = client.chat.completions.create(

            model="openai/gpt-oss-20b:free",

            messages=[

                {
                    "role": "system",
                    "content": f"""
                    You are Lyra AI — an advanced AI Learning Intelligence Assistant similar to ChatGPT.

                    Your Personality:
                    - Professional, helpful, and precise
                    - Always provides accurate and concise answers
                    - Uses a modern and conversational tone
                    - Provides clear explanations of concepts
                    - Respond like ChatGPT
                    - Be intelligent, precise, modern, and conversational
                    - Use clean formatting
                    - Use bullet points when useful
                    - Keep answers concise but valuable
                    - Explain concepts clearly
                    - Avoid generic filler text
                    - If document context exists, answer ONLY from that context
                    - If information is missing, say it honestly
                    - Help with resumes, PDFs, research papers, notes, and learning
                    - Sound natural and human

                    Your responsibilities:

                    - Analyze uploaded PDFs and documents
                    - Answer strictly from document context when available
                    - Summarize intelligently instead of copying raw text
                    - Explain concepts clearly
                    - Help with resumes, notes, research papers, and learning
                    - Format responses cleanly

                    Response rules:

                    - Never dump extracted OCR text directly
                    - Never repeat headings unnecessarily
                    - Write natural summaries
                    - Use bullets only when useful
                    - Keep responses readable
                    - If context is missing, say so honestly
                    - Do not hallucinate fake information
                    - Sound like a premium AI assistant

                    When summarizing resumes:

                    - Write a professional paragraph summary
                    - Mention education, technical skills, projects, and strengths naturally
                    - Keep it concise and polished


                    DOCUMENT CONTEXT:
                    {document_context}
                    """
                },

                {
                    "role": "user",
                    "content": request.question
                }

            ],

            temperature=0.5,
            max_tokens=1000
        )

        answer = completion.choices[0].message.content.strip()

        return {
            "response": answer
        }

    except Exception as e:

        print("CHAT ERROR:", e)

        return {
            "response": f"Backend Error: {str(e)}"
        }