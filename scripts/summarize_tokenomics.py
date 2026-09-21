import argparse,json
from collections import defaultdict
from app.config import settings
p=argparse.ArgumentParser(); p.add_argument("--require-10",action="store_true"); a=p.parse_args()
try:
    rows=[json.loads(x) for x in open(settings.token_log_path,encoding="utf-8") if x.strip()]
except FileNotFoundError: raise SystemExit("No token log found.")
if a.require_10 and len(rows)<10: raise SystemExit(f"Need at least 10 records; found {len(rows)}")
print("Total Bedrock calls:",len(rows))
print("Total input tokens:",sum(x["input_tokens"] for x in rows))
print("Total output tokens:",sum(x["output_tokens"] for x in rows))
print("Estimated total cost: $%.6f"%sum(x["estimated_cost_usd"] for x in rows))
by=defaultdict(lambda:[0,0,0,0.0])
for x in rows:
    y=by[x["operation"]]; y[0]+=1; y[1]+=x["input_tokens"]; y[2]+=x["output_tokens"]; y[3]+=x["estimated_cost_usd"]
for k,v in sorted(by.items()): print(k,v)
