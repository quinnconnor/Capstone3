import json,os
from datetime import datetime,timezone
from .config import settings

def record_usage(operation,input_tokens,output_tokens,model):
    cost=input_tokens/1_000_000*settings.input_price+output_tokens/1_000_000*settings.output_price
    row={"timestamp":datetime.now(timezone.utc).isoformat(),"operation":operation,
         "model":model,"input_tokens":int(input_tokens),"output_tokens":int(output_tokens),
         "estimated_cost_usd":round(cost,8)}
    d=os.path.dirname(settings.token_log_path)
    if d: os.makedirs(d,exist_ok=True)
    with open(settings.token_log_path,"a",encoding="utf-8") as f: f.write(json.dumps(row)+"\n")
    return row
