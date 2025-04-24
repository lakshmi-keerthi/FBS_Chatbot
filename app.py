import streamlit as st
import google.generativeai as genai
import faiss
import numpy as np
import os

# Set Streamlit page config
st.set_page_config(page_title="Chatty – FBS Financial Assistant", layout="centered")

# Load Prompt and Content
with open("FBS_Prompt_v2.md", "r", encoding="utf-8") as f:
    chatty_prompt = f.read()

with open("Webpage.md", "r", encoding="utf-8") as f:
    fbs_content = f.read()

# Sidebar for API Key Entry
st.sidebar.title("🔐 API Configuration")
GOOGLE_API_KEY = st.sidebar.text_input("Enter your Google API Key:", type="password")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

    # Split FBS content based on headings
    chunks = fbs_content.split('####')
    chunks = [f"#### {chunk.strip()}" for chunk in chunks if chunk.strip()]

    @st.cache_resource
    def embed_chunks(chunks):
        embeddings = [genai.embed_content(model="models/text-embedding-004", content=chunk, task_type="retrieval_document")['embedding'] for chunk in chunks]
        embeddings = np.array(embeddings)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return index, embeddings

    index, chunk_embeddings = embed_chunks(chunks)

    def retrieve_chunks(query, k=5):
        query_embedding = np.array([genai.embed_content(model="models/text-embedding-004", content=query, task_type="retrieval_query")['embedding']])
        D, I = index.search(query_embedding, k)
        return [chunks[i] for i in I[0]]

    def chatty_response(user_query):
    context = "\n".join(retrieve_chunks(user_query))

    # Reconstruct previous messages for history
    history = ""
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Chatty"
        history += f"{role}: {msg['content']}\n"

    # Build full prompt with history
    full_prompt = f"{chatty_prompt}\n\n{history}\nUser: {user_query}\n\nContext:\n{context}\n\nChatty:"
    
    response = genai.GenerativeModel("gemini-1.5-pro-latest").generate_content(
        full_prompt, generation_config=genai.types.GenerationConfig(
            temperature=0.3))
    return response.text.strip()


    # 🎨 Chat UI Header
    st.title("💬 Chatty – Your FBS Financial Assistant")
    st.markdown("Get general financial advice based on FBS offerings. I'm Chatty, how can I assist you today?")

    # Initialize chat session
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display all chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if user_input := st.chat_input("Ask me about FBS investments, retirement, or planning..."):
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Chatty is thinking..."):
            response_text = chatty_response(user_input)

        with st.chat_message("assistant"):
            st.markdown(response_text)

        st.session_state.messages.append({"role": "assistant", "content": response_text})

else:
    st.warning("Please enter your Google API key in the sidebar to continue.")
