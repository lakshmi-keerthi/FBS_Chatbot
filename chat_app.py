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
    st.experimental_rerun()  # Immediate rerun with new state

# ---- Stage 1: Financial Priority ---- #
if st.session_state.stage == "start":
    st.title("💬 Chatty – FBS Financial Assistant")
    st.subheader("What is your financial priority?")

    if st.button("Investments"):
        go_to_stage("goal", "priority", "Investments")
    if st.button("Retirement Solutions"):
        go_to_stage("goal", "priority", "Retirement Solutions")
    if st.button("Financial Planning"):
        go_to_stage("goal", "priority", "Financial Planning")

# ---- Stage 2: Goal Selection ---- #
elif st.session_state.stage == "goal":
    priority = st.session_state.flow_data["priority"]
    st.title(f"💬 Chatty – {priority}")
    st.subheader("What's your next step?")

    if priority == "Investments":
        if st.button("Recurring Income"):
            go_to_stage("details", "goal", "Recurring Income")
        if st.button("Long-term Investment"):
            go_to_stage("details", "goal", "Long-term Investment")
        if st.button("Portfolio Management"):
            go_to_stage("details", "goal", "Portfolio Management")

    elif priority == "Retirement Solutions":
        if st.button("Self-employed (1099)"):
            go_to_stage("details", "goal", "Self-employed (1099)")
        if st.button("W2"):
            go_to_stage("details", "goal", "W2")
        if st.button("Business owner"):
            go_to_stage("details", "goal", "Business owner")

    elif priority == "Financial Planning":
        if st.button("One-Time Comprehensive Plan"):
            go_to_stage("details", "goal", "One-Time Comprehensive Plan")
        if st.button("Annual Planning & Tracking"):
            go_to_stage("details", "goal", "Annual Planning & Tracking")
        if st.button("Estate Planning"):
            go_to_stage("details", "goal", "Estate Planning")

# ---- Stage 3: Details ---- #
elif st.session_state.stage == "details":
    priority = st.session_state.flow_data["priority"]
    goal = st.session_state.flow_data["goal"]
    st.title(f"{priority} → {goal}")
    st.subheader("Details:")

    # ---- Show Info Based on Flow ---- #
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

    # ---- Proceed to Chat ---- #
    if st.button("Continue to Chat with Chatty"):
        go_to_stage("chat")

# ---- Stage 4: Chatty AI Chat ---- #
elif st.session_state.stage == "chat":
    st.title("💬 Chatty – AI Financial Assistant")
    st.subheader("Ask me more about FBS services...")
