# 1. Set up some fake building blocks
# 2. create a fake model (that keeps going)
# 3. sub in our fakes from step 1
# 4. hit our endpoint
# 5. check it stopped
# pretend the model never stops - check if code stops it anyway

from fastapi.testclient import TestClient

import agent
from main import app

client = TestClient(app)

# 1. fake building blocks - only the attributes agent.py actually reads
class FakeUsage:
    def __init__(self, i, o):
        self.input_tokens, self.output_tokens = i, o


class FakeToolUseBlock:
    type = "tool_use"          # no trailing commas
    id = "toolu_01"
    name = "search_knowledge_base"

    def __init__(self, input_):
        self.input = input_


class FakeResponse:
    def __init__(self, content, stop_reason, usage):
        self.content, self.stop_reason, self.usage = content, stop_reason, usage


def test_agent_stops_at_max_iterations_instead_of_looping_forever(monkeypatch):
    calls = []

    # 2. a fake model that asks for a tool every single time
    def fake_create(**kwargs):
        calls.append(kwargs)
        return FakeResponse(
            [FakeToolUseBlock({"query": "anything"})],
            "tool_use",
            FakeUsage(100, 15),
        )

    # 3. swap in the fakes
    monkeypatch.setattr(agent.client.messages, "create", fake_create)
    monkeypatch.setattr(
        agent.knowledge,
        "search",
        lambda query, top_k=3: [{"id": "doc-001", "title": "t", "text": "x", "score": 0.5}],
    )
    
    response = client.post("/agent/ask", json={"question": "never resolves"})
    body = response.json()

    # assert - completed
    assert body["completed"] is False
    
    # assert - stop_reason
    assert body["stop_reason"] == "max_iterations"
    
    # assert - tool_Calls_made
    assert body["total_calls_made"] == agent.MAX_ITERATIONS