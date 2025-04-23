import streamlit as st
import google.generativeai as genai
import faiss
import numpy as np
import os

# Set Streamlit page config
st.set_page_config(page_title="Chatty - FBS Financial Assistant", layout="wide")

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

    # Embed chunks using Google Embeddings (cached)
    @st.cache_resource
    def embed_chunks(chunks):
        embeddings = [genai.embed_content(model="models/embedding-001", content=chunk, task_type="retrieval_document")['embedding'] for chunk in chunks]
        embeddings = np.array(embeddings)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return index, embeddings

    index, chunk_embeddings = embed_chunks(chunks)

    # Retrieve relevant chunks
    def retrieve_chunks(query, k=5):
        query_embedding = np.array([genai.embed_content(model="models/embedding-001", content=query, task_type="retrieval_query")['embedding']])
        D, I = index.search(query_embedding, k)
        return [chunks[i] for i in I[0]]

    # Generate Chatty response using Gemini
    def chatty_response(user_query):
        context = "\n".join(retrieve_chunks(user_query))
        full_prompt = f"{chatty_prompt}\n\nContext:\n{context}\n\nUser: {user_query}\nChatty:"
        response = genai.GenerativeModel("gemini-1.5-pro-latest").generate_content(full_prompt)
        return response.text.strip()

    # Streamlit Chat UI
    st.title("💬 Chatty - FBS Financial Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat messages
    for role, text in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"<div style='text-align: right; background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin: 5px;'>{text}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; background-color: #F1F0F0; padding: 10px; border-radius: 10px; margin: 5px;'>{text}</div>", unsafe_allow_html=True)

    # Input box at bottom
    user_input = st.text_input("Type your message here...", key="input", placeholder="Ask Chatty anything about FBS...")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        answer = chatty_response(user_input)
        st.session_state.chat_history.append(("chatty", answer))
        st.experimental_rerun()

else:
    st.warning("Please enter your Google API key in the sidebar to continue.")
