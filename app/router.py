import json
from .bedrock import BedrockClaude
def route_question(question):
    p=f"""Classify into exactly one: opensearch, redshift, both.
opensearch=document/policy text; redshift=structured/tabular data; both=must combine both.
Return ONLY JSON {{"route":"opensearch|redshift|both","reason":"brief"}}.
Question: {question}"""
    raw=BedrockClaude().invoke(p,"classification",180)["text"].strip()
    try: route=json.loads(raw)["route"].lower()
    except Exception: route="both" if "both" in raw.lower() else ("redshift" if "redshift" in raw.lower() else "opensearch")
    return route if route in {"opensearch","redshift","both"} else "both"
