import time
import random
import logging
from anthropic import Anthropic, APIStatusError, APIConnectionError, RateLimitError

logger = logging.getLogger(__name__)

# $ per million tokens (input, output) — update if Anthropic changes pricing
# Source: https://docs.claude.com/en/docs/about-claude/pricing
PRICING_PER_MTOK = {
    "claude-opus-4-6":    (5.00, 25.00),
    "claude-sonnet-4-6":  (3.00, 15.00),
    "claude-haiku-4-5":   (1.00, 5.00),
}

def call_with_retry_and_cost_logging(
    client: Anthropic,
    model: str,
    max_tokens: int,
    messages: list[dict],
    max_retries: int = 5,
    base_delay: float = 1.0,
    **kwargs,
):
    last_exception: RateLimitError | APIConnectionError | APIStatusError | None = None

    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=messages,
                **kwargs,
            )
            # ... cost logging unchanged ...
            return response

        except (RateLimitError, APIConnectionError) as e:
            last_exception = e
        except APIStatusError as e:
            if e.status_code < 500:
                raise
            last_exception = e

        if attempt < max_retries - 1:
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
            time.sleep(delay)

    # Loop only exits here if every attempt set last_exception — but assert it for the type checker
    assert last_exception is not None
    raise last_exception