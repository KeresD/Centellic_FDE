"""Everything tunable comes from the environment. No secrets in code."""

import os

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
EMBED_MODEL = os.environ.get("VOYAGE_MODEL", "voyage-3-lite")

# minimum similarity (1 - cosine distance) before a document reaches Claude
RELEVANCE_FLOOR = float(os.environ.get("RELEVANCE_FLOOR", "0.33"))

# holdings are quarterly; older than this and the compliance result carries a warning
HOLDINGS_STALE_DAYS = int(os.environ.get("HOLDINGS_STALE_DAYS", "45"))

AGENT_MAX_ITERATIONS = int(os.environ.get("AGENT_MAX_ITERATIONS", "5"))

CHROMA_PATH = os.environ.get("CHROMA_PATH", "./chroma_store")
CHROMA_COLLECTION = os.environ.get("CHROMA_COLLECTION", "wrenford_documents")
SEARCH_TOP_K = int(os.environ.get("SEARCH_TOP_K", "3"))

# the firm's timezone: defines "today" for staleness checks and date stamps
BUSINESS_TIMEZONE = os.environ.get("BUSINESS_TIMEZONE", "Europe/London")