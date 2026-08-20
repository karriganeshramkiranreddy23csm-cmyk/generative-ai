import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def get_llm_response(messages):
    """
    Sends the conversation history (including the system prompt and the latest user message)
    to the Groq LLM API and returns the response content.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="openai/gpt-oss-20b",
            temperature=0.3,
            max_tokens=512,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ Unable to contact the AI service right now. Error: {str(e)}"
