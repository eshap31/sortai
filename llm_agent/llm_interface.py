from openai import OpenAI
from dotenv import load_dotenv
import os, json
from llm_agent.prompt_builder import build_prompt

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_invoice(invoice_text: str, known_llcs: list[str]) -> dict:
    prompt = build_prompt(invoice_text, known_llcs)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.choices[0].message.content

    # Clean out triple backticks and optional language labels
    if content.startswith("```"):
        content = content.strip("`").strip()
        content = content.replace("json", "", 1).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        print("Raw LLM response:", content)
        raise
