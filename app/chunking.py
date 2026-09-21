import re

def approx_tokens(text):
    return len(re.findall(r"\S+", text))

def _chunk(words,n):
    text=" ".join(words)
    return {"chunk_number":n,"text":text,"token_count":approx_tokens(text)}

def chunk_text(text,min_tokens=500,max_tokens=900,overlap_tokens=75):
    text=re.sub(r"\s+"," ",text).strip()
    if not text: return []
    sentences=re.split(r"(?<=[.!?])\s+",text)
    out=[]; cur=[]; n=0
    for sentence in sentences:
        words=sentence.split()
        while len(words)>max_tokens:
            out.append(_chunk(words[:max_tokens],n)); n+=1
            words=words[max_tokens-overlap_tokens:]
        if not cur or len(cur)+len(words)<=max_tokens:
            cur.extend(words)
        else:
            out.append(_chunk(cur,n)); n+=1
            cur=cur[-overlap_tokens:]+words if overlap_tokens else words
    if cur: out.append(_chunk(cur,n))
    if len(out)>=2 and out[-1]["token_count"]<min_tokens:
        merged=out[-2]["text"]+" "+out[-1]["text"]
        if approx_tokens(merged)<=max_tokens:
            out[-2]=_chunk(merged.split(),out[-2]["chunk_number"]); out.pop()
    return out
