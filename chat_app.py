import streamlit as st

# Session State Initialization
if "stage" not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.flow_data = {}
    st.session_state.messages = []

# ---- Flowchart Section ---- #
st.set_page_config(page_title="Chatty – FBS Financial Assistant", layout="centered")
st.title("💬 Chatty – FBS Financial Assistant")

# --- Stage 1: Financial Priority --- #
if st.session_state.stage == "start":
    st.subheader("What is your financial priority?")
    priority = st.radio("Choose one:", ["Investments", "Retirement Solutions", "Financial Planning"])
    if st.button("Next"):
        st.session_state.flow_data["priority"] = priority
        st.session_state.stage = "goal"

# --- Stage 2: Goal Based on Priority --- #
elif st.session_state.stage == "goal":
    priority = st.session_state.flow_data["priority"]
    st.subheader(f"Your Priority: {priority}")

    if priority == "Investments":
        goal = st.radio("What's your primary goal?", ["Recurring Income", "Long-term Investment", "Portfolio Management"])
    elif priority == "Retirement Solutions":
        goal = st.radio("What is your employment status?", ["Self-employed (1099)", "W2", "Business owner"])
    elif priority == "Financial Planning":
        goal = st.radio("Are you looking for:", ["One-Time Comprehensive Plan", "Annual Planning & Tracking", "Estate Planning"])

    if st.button("Next"):
        st.session_state.flow_data["goal"] = goal
        st.session_state.stage = "details"

# --- Stage 3: Show Flow-Based Info --- #
elif st.session_state.stage == "details":
    priority = st.session_state.flow_data["priority"]
    goal = st.session_state.flow_data["goal"]
    st.subheader(f"{priority} → {goal}")

    # --- Display messages based on flow --- #
    if priority == "Investments":
        if goal == "Recurring Income":
            st.info("Our investment solutions:\n• Private Credit\n• Structured Note\n• Unsure – Check with Ruchitha.")
        elif goal == "Long-term Investment":
            st.info("Our services:\n• Private Funds\n• Model Portfolio")
        elif goal == "Portfolio Management":
            st.info("Portfolio Management:\n• Diversified Portfolios\n• GRO model strategy\n• Clear performance insights.")

    elif priority == "Retirement Solutions":
        if goal == "Self-employed (1099)":
            st.info("Solo 401(k) options available.\n• Increase Contributions\n• Reduce Taxes\n• Unsure – Let's discuss.")
        elif goal == "W2":
            st.info("• Changing employer? → Talk to an expert.\n• 401(k) transfer? → Talk to an expert.\n• 401(k) reduced? → Strategic Roth Conversions.")
        elif goal == "Business owner":
            st.info("• Solo 401(k) or plans to attract talent?\n• Traditional 401(k), CBP, Pension options available.")

    elif priority == "Financial Planning":
        if goal == "One-Time Comprehensive Plan":
            st.info("Includes:\n• Retirement projections\n• Investment reviews\n• Flat Fee: $5,000")
        elif goal == "Annual Planning & Tracking":
            st.info("Ongoing personalized advice.\n• Fee: $1,000 annually\n• Exclusive after One-Time Plan.")
        elif goal == "Estate Planning":
            st.info("Package includes:\n• Living Trust\n• Will\n• Power of Attorney\n• Fee: $2,500")

    if st.button("Continue to Chat with Chatty"):
        st.session_state.stage = "chat"

# --- Stage 4: AI Chat After Flow --- #
elif st.session_state.stage == "chat":
    st.subheader("Ask Chatty More About FBS Services!")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input for AI
    if user_input := st.chat_input("Ask me about FBS investments, retirement, or planning..."):
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Chatty is thinking..."):
            # --- Placeholder AI Response (replace with real AI call if needed) --- #
            ai_reply = f"Thanks for your question about '{user_input}'. Here's some information based on FBS offerings..."
        
        st.chat_message("assistant").markdown(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
