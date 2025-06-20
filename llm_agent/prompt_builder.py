def build_prompt(invoice_text: str, known_llcs: list[str]) -> str:
    prompt = f"""
You are an intelligent invoice classification agent.

Your task is to:
1. Extract the invoice fields from the text.
2. Match the invoice to the correct LLC from the known list.
3. Return a JSON object with the fields: `llc_name`, `invoice_summary`, and `reasoning`.

### Known LLCs:
{chr(10).join(['- ' + llc for llc in known_llcs])}

### Invoice Text:
\"\"\"
{invoice_text}
\"\"\"

### Output Format:
{{
  "llc_name": string,
  "invoice_summary": {{
    "vendor": string,
    "amount": string,
    "date": string,
    "address": string
  }},
  "reasoning": string
}}

Only return the JSON.
    """
    return prompt.strip()
