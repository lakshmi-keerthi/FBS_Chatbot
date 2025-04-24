import streamlit as st

# Set up session state
if "stage" not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.flow_data = {}

# Button handler function
def go_to_stage(stage_name, key, value=None):
    if value:
        st.session_state.flow_data[key] = value
    st.session_state.stage = stage_name

# Start Stage
if st.session_state.stage == "start":
    st.subheader("What is your financial priority?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Investments"):
            go_to_stage("goal", "priority", "Investments")
    with col2:
        if st.button("Retirement Solutions"):
            go_to_stage("goal", "priority", "Retirement Solutions")
    with col3:
        if st.button("Financial Planning"):
            go_to_stage("goal", "priority", "Financial Planning")

# Goal Stage
elif st.session_state.stage == "goal":
    st.subheader(f"Your Priority: {st.session_state.flow_data['priority']}")
    st.write("What's your next step?")
    if st.session_state.flow_data['priority'] == "Investments":
        if st.button("Recurring Income"):
            go_to_stage("details", "goal", "Recurring Income")
        if st.button("Long-term Investment"):
            go_to_stage("details", "goal", "Long-term Investment")
        if st.button("Portfolio Management"):
            go_to_stage("details", "goal", "Portfolio Management")
    elif st.session_state.flow_data['priority'] == "Retirement Solutions":
        if st.button("Self-employed (1099)"):
            go_to_stage("details", "goal", "Self-employed (1099)")
        if st.button("W2"):
            go_to_stage("details", "goal", "W2")
        if st.button("Business owner"):
            go_to_stage("details", "goal", "Business owner")
    elif st.session_state.flow_data['priority'] == "Financial Planning":
        if st.button("One-Time Comprehensive Plan"):
            go_to_stage("details", "goal", "One-Time Comprehensive Plan")
        if st.button("Annual Planning & Tracking"):
            go_to_stage("details", "goal", "Annual Planning & Tracking")
        if st.button("Estate Planning"):
            go_to_stage("details", "goal", "Estate Planning")

# Details Stage
elif st.session_state.stage == "details":
    priority = st.session_state.flow_data["priority"]
    goal = st.session_state.flow_data["goal"]
    st.subheader(f"{priority} → {goal}")
    st.info(f"Details for {goal} under {priority} will be displayed here.")

    if st.button("Continue to Chat"):
        st.session_state.stage = "chat"

# Chat Stage
elif st.session_state.stage == "chat":
    st.subheader("Welcome to Chatty – AI Chat Enabled!")
    st.write("Start asking me questions about FBS services...")
    user_query = st.text_input("Your Question:")
    if user_query:
        st.write(f"Chatty: I'm processing your query – '{user_query}'")
