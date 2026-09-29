"""The tool-use loop - nothing in here knows about FastAPI"""

from typing import Any
import knowledge_store as knowledge
from llm import MODEL, client

AGENT_SYSTEM_PROMPT = (
    "You are a legal market analyst with access to tools to search over a firm "
    "intelligence knowledge base. Use the tool whenever a question needs information "
    "you don't already have. Do not guess. Cite document ids in "
    "your final answer. If the tool returns nothing relevant, say so honestly. "
    "If the tool returns an error, tell the user the search failed and stop. "
    "Do not answer from general knowledge."
)

SEARCH_TOOL = {
    "name": "search_knowledge_base",
    "description": (
        "Search the firm intelligence knowledge base for documents relevant "
        "to a question about firms, jurisdictions, compliance, or market commentary."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query"},
        },
        "required": ["query"],
    },
}

# max model calls before giving up with stop_reason "max_iterations"
MAX_ITERATIONS = 4


def _execute_tools(name: str, tool_input: dict) -> tuple[str, bool]:
    """Run the requested tool. Returns (result_text, is_error)."""
    # Guard 1 - we only have one real tool
    if name != "search_knowledge_base":
        return f"Unknown tool: {name}", True

    # Guard 2 - the right tool is useless without its one argument
    if "query" not in tool_input:
        return 'Error: missing required field "query"', True

    # knowledge.search can raise RuntimeError - catch it here so it
    # goes back to the model instead of crashing the whole loop
    try:
        results = knowledge.search(tool_input["query"], top_k=3)
    except RuntimeError as e:
        return f"Error: {e}", True

    # A search that worked but found nothing - honest empty output, not an error
    if not results:
        return "No relevant documents found", False

    # The real success path - genuine results, formatted for the model to read
    formatted = "\n\n".join(
        f"[{r['id']}] {r['title']} (score {r['score']:.2f})\n{r['text']}"
        for r in results
    )
    return formatted, False


def ask_with_tools(question: str) -> dict:
    """Run the tool-use loop until the model answers, or the limit is hit."""
    messages: list[dict[str, Any]] = [{"role": "user", "content": question}]
    total_input_tokens = 0
    total_output_tokens = 0
    total_calls_made = 0

    for _ in range(MAX_ITERATIONS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=600,
            system=AGENT_SYSTEM_PROMPT,
            tools=[SEARCH_TOOL],
            messages=messages,
        )
        total_input_tokens += response.usage.input_tokens
        total_output_tokens += response.usage.output_tokens

        # the model is done - return its answer
        if response.stop_reason != "tool_use":
            final_text = next((b.text for b in response.content if b.type == "text"), "")
            return {
                "answer": final_text,
                "completed": True,
                "total_calls_made": total_calls_made,
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "stop_reason": response.stop_reason,
            }

        tool_blocks = [b for b in response.content if b.type == "tool_use"]
        tool_results: list = []
        # the model wants a tool - record its turn, run the tool(s), send results back
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for tool_block in tool_blocks:
            result_text, is_error = _execute_tools(tool_block.name, tool_block.input)
            if not is_error:
                total_calls_made += 1
                
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tool_block.id,
                    "content": result_text,
                    "is_error": is_error
                }
            )
            
        messages.append({"role": "user", "content": tool_results})
        
    # hit the iteration limit without a final answer
    return {
        "answer": "",
        "completed": False,
        "total_calls_made": total_calls_made,
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "stop_reason": "max_iterations",
    }
    



# The real success path = genuine results, formatted for the model to read