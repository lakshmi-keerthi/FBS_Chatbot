import streamlit as st
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

# Load your files
with open("FBS_Prompt_v2.md", "r", encoding="utf-8") as f:
    chatty_prompt = f.read()

with open("Webpage.md", "r", encoding="utf-8") as f:
    fbs_content = f.read()

# Set your Google API Key securely (or load from environment)
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"] if "GOOGLE_API_KEY" in st.secrets else st.text_input("Enter your Google API Key:", type="password")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

    # Split content by headings
    chunks = fbs_content.split('####')
    chunks = [f"#### {chunk.strip()}" for chunk in chunks if chunk.strip()]

    # Embed chunks using Google Embeddings
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

    # Generate Chatty's response
    def chatty_response(user_query):
        context = "\n".join(retrieve_chunks(user_query))
        full_prompt = f"{chatty_prompt}\n\nContext:\n{context}\n\nUser: {user_query}\nChatty:"
        response = genai.GenerativeModel("gemini-1.5-pro-latest").generate_content(full_prompt)
        return response.text.strip()

    # Streamlit UI
    st.title("💬 Chatty - FBS Financial Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask Chatty a financial question:")

    if st.button("Ask") and user_input:
        answer = chatty_response(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Chatty", answer))

    for speaker, text in st.session_state.chat_history:
        st.markdown(f"**{speaker}:** {text}")
