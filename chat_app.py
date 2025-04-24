import streamlit as st

# ---- Session Initialization ---- #
if "stage" not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.flow_data = {}
    st.session_state.messages = []

# ---- Helper to Move Between Stages ---- #
def go_to_stage(stage_name, key=None, value=None):
    if key and value:
        st.session_state.flow_data[key] = value
    st.session_state.stage = stage_name
    st.experimental_rerun()

# ---- Stage 1: Financial Priority ---- #
if st.session_state.stage == "start":
    st.title("💬 Chatty – FBS Financial Assistant")
    st.subheader("What is your financial priority?")

    if st.button("Investments"):
        go_to_stage("investments_goal", "priority", "Investments")
    if st.button("Retirement Solutions"):
        go_to_stage("retirement_status", "priority", "Retirement Solutions")
    if st.button("Financial Planning"):
        go_to_stage("financial_plan_type", "priority", "Financial Planning")

# ---- Stage 2: Investments Goals ---- #
elif st.session_state.stage == "investments_goal":
    st.title("Investments")
    st.subheader("What’s your primary goal?")

    if st.button("Recurring Income"):
        go_to_stage("recurring_income", "goal", "Recurring Income")
    if st.button("Long-term Investment"):
        go_to_stage("long_term", "goal", "Long-term Investment")
    if st.button("Portfolio Management"):
        go_to_stage("portfolio_mgmt", "goal", "Portfolio Management")

# ---- Recurring Income Options ---- #
elif st.session_state.stage == "recurring_income":
    st.title("Recurring Income")
    st.info("Our investment solutions:\n• Private Credit\n• Structured Note\n• Unsure – We'll help you decide.")
    if st.button("Continue to Chat"):
        go_to_stage("chat")

# ---- Long-term Investment Options ---- #
elif st.session_state.stage == "long_term":
    st.title("Long-term Investment")
    st.info("Our services:\n• Private Funds\n• Model Portfolio")
    if st.button("Continue to Chat"):
        go_to_stage("chat")

# ---- Portfolio Management Info ---- #
elif st.session_state.stage == "portfolio_mgmt":
    st.title("Portfolio Management")
    st.info("Diversified portfolios\nGRO model strategy\nClear performance insights.")
    if st.button("Continue to Chat"):
        go_to_stage("chat")

# ---- Stage 3: Retirement Solutions ---- #
elif st.session_state.stage == "retirement_status":
    st.title("Retirement Solutions")
    st.subheader("What is your employment status?")

    if st.button("Self-employed (1099)"):
        go_to_stage("self_employed", "status", "Self-employed")
    if st.button("W2"):
        go_to_stage("w2", "status", "W2")
    if st.button("Business owner"):
        go_to_stage("business_owner", "status", "Business owner")

# ---- Self-Employed Options ---- #
elif st.session_state.stage == "self_employed":
    st.title("Self-employed (1099)")
    st.subheader("Do you have a solo 401(k)?")
    if st.button("Yes"):
        st.info("Are you looking to:\n• Increase Contributions\n• Reduce Taxes\n• Unsure")
        if st.button("Continue to Chat"):
            go_to_stage("chat")
    if st.button("No"):
        st.info("Solo 401(k) can be a great choice for self-employed individuals.")
        if st.button("Continue to Chat"):
            go_to_stage("chat")

# ---- W2 Employee Options ---- #
elif st.session_state.stage == "w2":
    st.title("W2 Employee")
    st.subheader("What are you looking for?")
    if st.button("Changing employer"):
        st.info("Please talk to an expert at FBS.")
        go_to_stage("chat")
    if st.button("401(k) transfer"):
        st.info("Please talk to an expert at FBS.")
        go_to_stage("chat")
    if st.button("401(k) reduced in value"):
        st.info("Consider Strategic Roth Conversions. Let's explore options.")
        if st.button("Continue to Chat"):
            go_to_stage("chat")
    if st.button("None of the above"):
        st.info("Please talk to an expert at FBS.")
        go_to_stage("chat")

# ---- Business Owner Options ---- #
elif st.session_state.stage == "business_owner":
    st.title("Business Owner")
    st.subheader("Number of employees?")
    if st.button("1 Employee"):
        st.subheader("Do you have a solo 401(k)?")
        if st.button("Yes"):
            st.info("Looking to:\n• Increase Contributions\n• Reduce Taxes\n• Unsure")
            if st.button("Continue to Chat"):
                go_to_stage("chat")
        if st.button("No"):
            st.info("Solo 401(k) can be an excellent choice for your business.")
            if st.button("Continue to Chat"):
                go_to_stage("chat")
    if st.button("More than 1 Employee"):
        st.info("Are you looking to attract and retain talent using:\n• Traditional 401(k)\n• CBP\n• Pension")
        if st.button("Continue to Chat"):
            go_to_stage("chat")

# ---- Stage 4: Financial Planning ---- #
elif st.session_state.stage == "financial_plan_type":
    st.title("Financial Planning")
    st.subheader("Are you looking for:")
    if st.button("One-Time Comprehensive Plan"):
        st.info("Includes:\n• Retirement projections\n• Investment reviews\n• Fee: $5,000")
        go_to_stage("chat")
    if st.button("Annual Planning & Tracking"):
        st.info("Ongoing advice.\nFee: $1,000 annually\nExclusive after One-Time Plan.")
        go_to_stage("chat")
    if st.button("Estate Planning"):
        st.info("Includes:\n• Living Trust\n• Will\n• Power of Attorney\n• Fee: $2,500")
        go_to_stage("chat")

# ---- Final Stage: AI Chat ---- #
elif st.session_state.stage == "chat":
    st.title("💬 Chatty – AI Financial Assistant")
    st.subheader("Ask me more about FBS services...")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Placeholder for AI response – to be added later
    if user_input := st.chat_input("Ask your financial question..."):
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Chatty is thinking..."):
            response_text = f"Thanks for your question about '{user_input}'. Here's more about FBS services..."

        st.chat_message("assistant").markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
