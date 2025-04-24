import streamlit as st

# ---- Session Initialization ---- #
if "stage" not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.flow_data = {}
    st.session_state.messages = []

def safe_rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        st.rerun()

# ---- Helper to Move Between Stages ---- #
def go_to_stage(stage_name, key=None, value=None):
    if key and value:
        st.session_state.flow_data[key] = value
    st.session_state.stage = stage_name
    safe_rerun()

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

# ---- Investments Goal ---- #
elif st.session_state.stage == "investments_goal":
    st.title("Investments")
    st.subheader("What's your primary goal?")

    if st.button("Recurring Income"):
        go_to_stage("recurring_income", "goal", "Recurring Income")
    if st.button("Long-term Investment"):
        go_to_stage("details", "goal", "Long-term Investment")
    if st.button("Portfolio Management"):
        go_to_stage("details", "goal", "Portfolio Management")

# ---- Recurring Income Options ---- #
elif st.session_state.stage == "recurring_income":
    st.title("Recurring Income")
    st.info("Our investment solutions:\n• Private Credit\n• Structured Note")
    if st.button("Private Credit Details"):
        st.info("Private Credit:\nTargeted yields of 8% to 20%.\nDirect security interests in real estate.\nFlexible terms.\nMarket independence.")
    if st.button("Structured Note Options"):
        go_to_stage("structured_note")

    if st.button("Continue to Chat"):
        go_to_stage("chat")

# ---- Structured Note Sub-Options ---- #
elif st.session_state.stage == "structured_note":
    st.title("Structured Note")
    st.subheader("What would you like to do?")
    if st.button("Explore Upcoming Notes"):
        st.info("Please explore upcoming notes through your advisor.")
    if st.button("I have questions"):
        st.info("Feel free to ask Chatty more about Structured Notes in chat.")
    if st.button("Unsure"):
        st.info("Structured Notes combine traditional bonds with derivatives.\nSourced from JP Morgan, Goldman Sachs, etc.\nDiversification benefits.")
    if st.button("Back to Recurring Income"):
        go_to_stage("recurring_income")

# ---- Retirement Status ---- #
elif st.session_state.stage == "retirement_status":
    st.title("Retirement Solutions")
    st.subheader("What is your employment status?")

    if st.button("Self-employed (1099)"):
        go_to_stage("self_employed", "goal", "Self-employed (1099)")
    if st.button("W2"):
        go_to_stage("w2", "goal", "W2")
    if st.button("Business owner"):
        go_to_stage("business_owner", "goal", "Business owner")

# ---- Self-employed Flow ---- #
elif st.session_state.stage == "self_employed":
    st.title("Self-employed (1099)")
    st.subheader("Do you have a solo 401(k)?")
    if st.button("Yes"):
        st.info("Are you looking to:\n• Increase Contributions\n• Reduce Taxes\n• Unsure")
    if st.button("No"):
        st.info("Solo 401(k) offers tax-deferred growth for self-employed individuals.")

    if st.button("Continue to Chat"):
        go_to_stage("chat")

# ---- W2 Flow ---- #
elif st.session_state.stage == "w2":
    st.title("W2 Employee")
    st.subheader("What are you looking for?")
    if st.button("Changing employer"):
        st.info("Please talk to an expert at FBS.")
    if st.button("401(k) transfer"):
        st.info("Please talk to an expert at FBS.")
    if st.button("401(k) reduced in value"):
        st.info("Consider Strategic Roth Conversions for tax-free growth.")
    if st.button("None of the above"):
        st.info("Please talk to an expert at FBS.")

    if st.button("Continue to Chat"):
        go_to_stage("chat")

# ---- Business Owner Flow ---- #
elif st.session_state.stage == "business_owner":
    st.title("Business Owner")
    st.subheader("How many employees?")
    if st.button("1 Employee"):
        go_to_stage("self_employed")
    if st.button("More than 1 Employee"):
        st.info("Are you looking to attract and retain talent using:\n• Traditional 401(k)\n• CBP\n• Pension options.")
        if st.button("Continue to Chat"):
            go_to_stage("chat")

# ---- Financial Planning ---- #
elif st.session_state.stage == "financial_plan_type":
    st.title("Financial Planning")
    st.subheader("Are you looking for:")
    if st.button("One-Time Comprehensive Plan"):
        st.info("Includes:\n• Retirement projections\n• Tax optimization\n• Fee: $5,000")
        go_to_stage("chat")
    if st.button("Annual Planning & Tracking"):
        st.info("Ongoing support after comprehensive plan.\nFee: $1,000 annually")
        go_to_stage("chat")
    if st.button("Estate Planning"):
        st.info("Includes:\n• Living Trust\n• Will\n• Fee: $2,500")
        go_to_stage("chat")

# ---- Chat Stage ---- #
elif st.session_state.stage == "chat":
    st.title("💬 Chatty – AI Financial Assistant")
    st.subheader("Ask me more about FBS services...")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Ask your financial question..."):
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Chatty is thinking..."):
            response_text = f"Thanks for your question about '{user_input}'. Here's more about FBS services..."

        st.chat_message("assistant").markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
