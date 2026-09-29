from data import FIRMS
import llm

for chunk in llm.stream_firm_summary(FIRMS[0]):
    print(chunk, end="", flush=True)