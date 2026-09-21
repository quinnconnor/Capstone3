from app.bedrock import BedrockClaude
r=BedrockClaude().invoke("Reply with exactly: Bedrock smoke test passed.","smoke_test",50)
print(r["text"]); print({"input_tokens":r["input_tokens"],"output_tokens":r["output_tokens"]})
