from openai import OpenAI
from dotenv import load_dotenv
import os, json
from llm_agent.prompt_builder import build_prompt

# load the environment variables from .env file, and initialize openai client
# using my secret key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_invoice(invoice_text: str, known_llcs: list[str]) -> dict:
    """
    :param invoice_text: the text of the invoice
    :param known_llcs: list of llcs that the company manages
    :return: returns the GPT response (converts from json to python dictionary)
    :rtype: dict
    """

    # create the prompt, using the build_prompt function
    prompt = build_prompt(invoice_text, known_llcs)

    # send the prompt to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )

    #  Gets the actual text response (should be JSON) from the first result
    content = response.choices[0].message.content

    # Clean out triple backticks and optional language labels, that chat GPT usually
    # wraps JSON with
    if content.startswith("```"):
        content = content.strip("`").strip()
        content = content.replace("json", "", 1).strip()

    # try to convert the cleaned up string into a dictionary using json.loads
    # basically deserialize
    try:
        return json.loads(content)
    
    # if the response isn't in valid JSON format
    # prints the error and the raw string to help debug
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        print("Raw LLM response:", content)
        raise
