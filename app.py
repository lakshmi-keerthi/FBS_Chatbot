import streamlit as st
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# --- Setup Streamlit ---
st.set_page_config(page_title="💬 Chatty – LangChain-Powered FBS Assistant", layout="centered")
st.title("💬 Chatty – FBS Financial Assistant")
st.markdown("Ask me about FBS investments, retirement, or planning topics!")

# --- Sidebar API ---
st.sidebar.title("🔐 API Configuration")
GOOGLE_API_KEY = st.sidebar.text_input("Enter your Google API Key:", type="password")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

    # --- Load Prompt and FBS Content ---
    with open("FBS_Prompt_v2.md", "r", encoding="utf-8") as f:
        chatty_prompt = f.read()

    with open("Webpage.md", "r", encoding="utf-8") as f:
        fbs_content = f.read()

    # --- Split Content ---
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.create_documents([fbs_content])

    # --- Embedding and Vector Store ---
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vector_store = FAISS.from_documents(docs, embedding=embeddings)

    # --- Memory for Chat History ---
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # --- Prompt Template ---
    prompt_template = PromptTemplate.from_template("""
{chatty_prompt}

Context:
{context}

Chat History:
{chat_history}

User: {question}
Chatty:
""")

    # --- LLM Setup ---
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3, google_api_key=GOOGLE_API_KEY)

    # --- Conversational Retrieval Chain ---
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 5}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt_template.partial(chatty_prompt=chatty_prompt)}
    )

    # --- Streamlit Chat UI ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Ask me anything..."):
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Chatty is thinking..."):
            result = qa_chain({"question": user_input})
            response_text = result["answer"]

        st.chat_message("assistant").markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

else:
    st.warning("Please enter your Google API key in the sidebar to continue.")
