import httpx
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.title("Firm Intelligence")


# ---------- Feature 1: Ask ----------
st.write("## Ask")
question = st.text_input("Ask a question in plain English")

if st.button("Ask"):
    try:
        response = httpx.post(
            f"{API_URL}/agent/ask",
            json={"question": question},
            timeout=120.0,
        )
        response.raise_for_status()
        result = response.json()

        if result["completed"]:
            st.write(result["answer"])
        else:
            st.write("The agent hit its iteration limit before producing an answer. Try a narrower question.")

        st.write("Tool calls:", result["total_calls_made"])
        st.write("Input tokens:", result["input_tokens"])
        st.write("Output tokens:", result["output_tokens"])

    except httpx.HTTPStatusError as e:
        st.write(f"Error: API returned {e.response.status_code}: {e.response.text}")
    except httpx.TimeoutException:
        st.write("Error: the request timed out.")
    except httpx.RequestError:
        st.write(f"Error: could not reach the API at {API_URL}. Is uvicorn running?")


# ---------- Feature 2: Search only ----------
st.write("## Search only")
search_question = st.text_input("Search the knowledge base")

if st.button("Search"):
    try:
        response = httpx.post(
            f"{API_URL}/knowledge/search",
            json={"question": search_question},
            timeout=30.0,
        )

        if response.status_code == 409:
            st.write("The index hasn't been built yet. Call POST /knowledge/index, then try again.")
        else:
            response.raise_for_status()
            for r in response.json()["results"]:
                st.write(f"{r['title']} ({r['id']}), score {r['score']:.3f}")

    except httpx.HTTPStatusError as e:
        st.write(f"Error: search failed ({e.response.status_code}): {e.response.text}")
    except httpx.TimeoutException:
        st.write("Error: the search request timed out.")
    except httpx.RequestError:
        st.write(f"Error: could not reach the API at {API_URL}. Is uvicorn running?")


# ---------- Feature 3: Streaming summary ----------
st.write("## Streaming summary")
firm_id = st.text_input("Firm id")


def stream_summary(firm_id):
    with httpx.stream("GET", f"{API_URL}/firms/{firm_id}/summary/stream", timeout=60.0) as response:
        if response.status_code != 200:
            response.read()
            st.write(f"Error: API returned {response.status_code}: {response.text}")
            return
        for chunk in response.iter_text():
            yield chunk


if st.button("Stream summary"):
    try:
        st.write(stream_summary(firm_id))
    except httpx.RequestError:
        st.write(f"Error: could not reach the API at {API_URL}. Is uvicorn running?")