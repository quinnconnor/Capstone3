import re
BLOCKED_KEYWORDS=["DROP","DELETE","UPDATE","INSERT","ALTER","TRUNCATE","GRANT","REVOKE","CREATE","MERGE","CALL","COPY","UNLOAD"]

def validate_sql(query):
    if not isinstance(query,str) or not query.strip(): return {"valid":False,"reason":"Empty query"}
    q=query.strip().rstrip(";").strip()
    if ";" in q: return {"valid":False,"reason":"Multiple statements are not permitted"}
    q=re.sub(r"/\*.*?\*/"," ",q,flags=re.S)
    q=re.sub(r"--[^\n]*"," ",q).strip()
    u=q.upper()
    if not u.startswith("SELECT"): return {"valid":False,"reason":"Only SELECT queries are permitted"}
    for k in BLOCKED_KEYWORDS:
        if re.search(rf"\b{re.escape(k)}\b",u): return {"valid":False,"reason":f"Blocked: {k} not permitted"}
    return {"valid":True,"reason":"OK"}
