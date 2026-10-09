"""The tool-use loop. Nothing in here knows about FastAPI."""

from typing import Any

import config
from anthropic.types import MessageParam, ToolResultBlockParam
from llm import MODEL, client
from tools import TOOLS, run_tool

AGENT_SYSTEM_PROMPT = (
    "You support portfolio managers and advisers at Wrenford Asset Management. "
    "Use screen_portfolio for any question about whether a portfolio, or a proposed holding, "
    "meets a client mandate. Never judge compliance yourself: report each rule's status exactly "
    "as the tool returns it, and treat insufficient_evidence as unresolved, not as a pass. "
    "Use search_documents for what a policy, mandate or fund document says, and cite document "
    "ids in square brackets, like [doc-012]. Do not answer from general knowledge. "
    "If a tool returns an error, say what failed rather than guessing. "
    "Mandate compliance is not suitability: never say an investment is suitable for a client "
    "and never make a personal recommendation. "
    "Use British English. No em dash characters."
)


def ask_with_tools(question: str) -> dict:
    """Run the tool-use loop until Claude answers, or the iteration limit is hit."""
    messages: list[MessageParam] = [{"role": "user", "content": question}]
    total_input_tokens = 0
    total_output_tokens = 0
    total_calls_made = 0
    tool_calls: list[dict] = []    # name, input and is_error for each call, for the UI

    for _ in range(config.AGENT_MAX_ITERATIONS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            system=AGENT_SYSTEM_PROMPT,
            tools=TOOLS, # type: ignore[arg-type]
            messages=messages,
        )
        total_input_tokens += response.usage.input_tokens
        total_output_tokens += response.usage.output_tokens

        # Claude is done - return its answer
        if response.stop_reason != "tool_use":
            final_text = "".join(b.text for b in response.content if b.type == "text")
            return {
                "answer": final_text,
                # only end_turn is a finished answer; max_tokens means it was cut off
                "completed": response.stop_reason == "end_turn",
                "total_calls_made": total_calls_made,
                "tool_calls": tool_calls,
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "stop_reason": response.stop_reason,
            }

        # Claude wants tools - record its turn, run every tool it asked for, send results back
        messages.append({"role": "assistant", "content": response.content})
        tool_results: list[ToolResultBlockParam] = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            tool_input: dict[str, Any] = block.input if isinstance(block.input, dict) else {}
            result_text, is_error = run_tool(block.name, tool_input)
            total_calls_made += 1
            tool_calls.append({"name": block.name, "input": tool_input, "is_error": is_error})
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result_text,
                "is_error": is_error,
            })
        messages.append({"role": "user", "content": tool_results})

    # hit the iteration limit without a final answer
    return {
        "answer": "",
        "completed": False,
        "total_calls_made": total_calls_made,
        "tool_calls": tool_calls,
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "stop_reason": "max_iterations",
    }