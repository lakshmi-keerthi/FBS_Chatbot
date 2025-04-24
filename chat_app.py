import streamlit as st
import google.generativeai as genai
import faiss
import numpy as np

# ---- Page Config ---- #
st.set_page_config(page_title="Chatty – FBS Financial Assistant", layout="centered")
st.title("💬 Chatty – FBS Financial Assistant")

# ---- Session Initialization ---- #
if "stage" not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.flow_data = {}
    st.session_state.messages = []

# ---- Sidebar for API Key ---- #
st.sidebar.title("🔐 API Configuration")
GOOGLE_API_KEY = st.sidebar.text_input("Enter your Google API Key:", type="password")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

    # ---- Load Prompt and Content ---- #
    with open("FBS_Prompt_v2.md", "r", encoding="utf-8") as f:
        chatty_prompt = f.read()

    with open("Webpage.md", "r", encoding="utf-8") as f:
        fbs_content = f.read()

    # ---- Chunk Content ---- #
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
        history = ""
        for msg in st.session_state.messages[-4:]:
            role = "User" if msg["role"] == "user" else "Chatty"
            history += f"{role}: {msg['content']}\n"

        full_prompt = f"{chatty_prompt}\n\n{history}\nUser: {user_query}\n\nContext:\n{context}\n\nChatty:"
        response = genai.GenerativeModel("gemini-1.5-pro-latest").generate_content(
            full_prompt, generation_config=genai.types.GenerationConfig(temperature=0.3)
        )
        return response.text.strip()

    # ---- FLOWCHART SECTION ---- #
    if st.session_state.stage == "start":
        st.subheader("What is your financial priority?")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Investments"):
                st.session_state.flow_data["priority"] = "Investments"
                st.session_state.stage = "goal"

        with col2:
            if st.button("Retirement Solutions"):
                st.session_state.flow_data["priority"] = "Retirement Solutions"
                st.session_state.stage = "goal"

        with col3:
            if st.button("Financial Planning"):
                st.session_state.flow_data["priority"] = "Financial Planning"
                st.session_state.stage = "goal"

    elif st.session_state.stage == "goal":
        priority = st.session_state.flow_data["priority"]
        st.subheader(f"Your Priority: {priority}")
        st.write("What's your next step?")

        if priority == "Investments":
            if st.button("Recurring Income"):
                st.session_state.flow_data["goal"] = "Recurring Income"
                st.session_state.stage = "details"
            if st.button("Long-term Investment"):
                st.session_state.flow_data["goal"] = "Long-term Investment"
                st.session_state.stage = "details"
            if st.button("Portfolio Management"):
                st.session_state.flow_data["goal"] = "Portfolio Management"
                st.session_state.stage = "details"

        elif priority == "Retirement Solutions":
            if st.button("Self-employed (1099)"):
                st.session_state.flow_data["goal"] = "Self-employed (1099)"
                st.session_state.stage = "details"
            if st.button("W2"):
                st.session_state.flow_data["goal"] = "W2"
                st.session_state.stage = "details"
            if st.button("Business owner"):
                st.session_state.flow_data["goal"] = "Business owner"
                st.session_state.stage = "details"

        elif priority == "Financial Planning":
            if st.button("One-Time Comprehensive Plan"):
                st.session_state.flow_data["goal"] = "One-Time Comprehensive Plan"
                st.session_state.stage = "details"
            if st.button("Annual Planning & Tracking"):
                st.session_state.flow_data["goal"] = "Annual Planning & Tracking"
                st.session_state.stage = "details"
            if st.button("Estate Planning"):
                st.session_state.flow_data["goal"] = "Estate Planning"
                st.session_state.stage = "details"

    elif st.session_state.stage == "details":
        priority = st.session_state.flow_data["priority"]
        goal = st.session_state.flow_data["goal"]
        st.subheader(f"{priority} → {goal}")

        if priority == "Investments":
            if goal == "Recurring Income":
                st.info("Our investment solutions:\n• Private Credit\n• Structured Note\n• Unsure – Check with Ruchitha.")
            elif goal == "Long-term Investment":
                st.info("Our services:\n• Private Funds\n• Model Portfolio")
            elif goal == "Portfolio Management":
                st.info("Diversified portfolios\nGRO model strategy\nClear performance insights.")

        elif priority == "Retirement Solutions":
            if goal == "Self-employed (1099)":
                st.info("Solo 401(k):\n• Increase Contributions\n• Reduce Taxes\n• Unsure – Let's discuss.")
            elif goal == "W2":
                st.info("• Changing employer? → Talk to an expert.\n• 401(k) transfer? → Talk to an expert.\n• 401(k) reduced? → Strategic Roth Conversions.")
            elif goal == "Business owner":
                st.info("Solo 401(k) or plans to attract talent:\n• Traditional 401(k)\n• CBP\n• Pension options.")

        elif priority == "Financial Planning":
            if goal == "One-Time Comprehensive Plan":
                st.info("Includes:\n• Retirement projections\n• Investment reviews\n• Flat Fee: $5,000")
            elif goal == "Annual Planning & Tracking":
                st.info("Ongoing advice.\nFee: $1,000 annually\nExclusive after One-Time Plan.")
            elif goal == "Estate Planning":
                st.info("Package includes:\n• Living Trust\n• Will\n• Power of Attorney\n• Fee: $2,500")

        if st.button("Continue to Chat with Chatty"):
            st.session_state.stage = "chat"

    elif st.session_state.stage == "chat":
        st.subheader("Ask Chatty More About FBS Services!")

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if user_input := st.chat_input("Ask me about FBS investments, retirement, or planning..."):
            st.chat_message("user").markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})

            with st.spinner("Chatty is thinking..."):
                response_text = chatty_response(user_input)

            st.chat_message("assistant").markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

else:
    st.warning("Please enter your Google API key in the sidebar to continue.")
