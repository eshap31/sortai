def build_prompt(invoice_text: str, known_llcs: list[str]):
    """
      function get's the text of the invoice, and the list of llcs
      and builds and returns a natural language prompt for GPT
      :params invoice_text: the invoice in text form
      :type invoice_text: string
      :params known_llcs: list of llcs that the company manages
      :type known_llcs: list[str]
      :return: natural language prompt for GPT
      :rtype: str
    """
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
