def build_prompt(invoice_text: str, llc_metadata: dict) -> str:
    """
    Builds a prompt for the LLM to classify an invoice based on known LLCs and their associated addresses.
    :param invoice_text: The raw text of the invoice to be classified.
    :type invoice_text: str
    :param llc_metadata: A dictionary mapping LLC names to their associated addresses.
    :type llc_metadata: dict
    :return: A formatted prompt string for the LLM.
    :rtype: str
    """

    formatted_llcs = "\n".join([
        f"- {llc}\n  - Associated addresses: {', '.join(addresses)}"
        for llc, addresses in llc_metadata.items()
    ])

    prompt = f"""
You are an invoice classification agent.

Given a list of LLCs with their associated addresses, and the raw text of an invoice, extract the invoice fields and assign the correct LLC based on address or vendor match.

### Known LLCs and Addresses:
{formatted_llcs}

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
    "address": string,
    "invoice_number": string,
    "order_number": string
  }},
  "reasoning": string
}}

If any fields like invoice number or order number are not available, return null or an empty string.
Only return valid JSON.
"""
    return prompt.strip()
