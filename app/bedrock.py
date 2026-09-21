import json,boto3
from .config import settings
from .tokenomics import record_usage

class BedrockClaude:
    def __init__(self):
        self.client=boto3.client("bedrock-runtime",region_name=settings.region)
        if not settings.bedrock_model_id: raise ValueError("BEDROCK_MODEL_ID is required")
    def invoke(self,prompt,operation,max_tokens=700):
        body={"anthropic_version":"bedrock-2023-05-31","max_tokens":max_tokens,
              "messages":[{"role":"user","content":prompt}]}
        r=self.client.invoke_model(modelId=settings.bedrock_model_id,body=json.dumps(body),
                                   contentType="application/json",accept="application/json")
        x=json.loads(r["body"].read()); u=x.get("usage",{})
        record_usage(operation,u.get("input_tokens",0),u.get("output_tokens",0),settings.bedrock_model_id)
        return {"text":x["content"][0]["text"],"input_tokens":u.get("input_tokens",0),
                "output_tokens":u.get("output_tokens",0)}
