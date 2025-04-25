import streamlit as st
import google.generativeai as genai
from langchain_community.embeddings import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain

# ---- Streamlit Page Config ---- #
st.set_page_config(page_title="Chatty – FBS Financial Assistant", layout="centered")

# ---- Sidebar for API Key ---- #
st.sidebar.title("🔐 API Configuration")
GOOGLE_API_KEY = st.sidebar.text_input("Enter your Google API Key:", type="password")

# ---- Load Prompt & Knowledge Base ---- #
with open("FBS_Prompt_v2.md", "r", encoding="utf-8") as f:
    chatty_prompt = f.read()

with open("Webpage.md", "r", encoding="utf-8") as f:
    fbs_content = f.read()

# ---- Initialize Only If API Key ---- #
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

    # --- Chunk Content --- #
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.create_documents([fbs_content])

    # --- Embedding and Vector Store --- #
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=GOOGLE_API_KEY
    )
    vector_store = FAISS.from_documents(docs, embedding=embeddings)

    # --- Memory for Chat History --- #
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True
    )

    # --- Chat Model (Gemini Pro) --- #
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        temperature=0.3,
        google_api_key=GOOGLE_API_KEY
    )

    # --- Prompt Template --- #
    prompt = ChatPromptTemplate.from_messages([
        ("system", chatty_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])

    # --- Conversational Retrieval Chain --- #
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt}
    )

    # ---- Streamlit Chat UI ---- #
    st.title("💬 Chatty – Your FBS Financial Assistant")
    st.markdown("Get general financial advice based on FBS offerings. I'm Chatty, how can I assist you today?")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display all chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if user_input := st.chat_input("Ask me about FBS investments, retirement, or planning..."):
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Chatty is thinking..."):
            result = qa_chain({"question": user_input})
            response_text = result["answer"]

        st.chat_message("assistant").markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

else:
    st.warning("Please enter your Google API key in the sidebar to continue.")
