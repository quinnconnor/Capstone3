import argparse,json
from app.query_engine import QueryEngine
p=argparse.ArgumentParser(); p.add_argument("question"); a=p.parse_args()
r=QueryEngine().answer(a.question)
print(json.dumps(r,indent=2,default=str)); print("\nFINAL ANSWER\n"); print(r["answer"])
