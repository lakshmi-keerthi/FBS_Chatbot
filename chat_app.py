import streamlit as st

# ---- Session Initialization ---- #
if "stage" not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.flow_data = {}
    st.session_state.messages = []

# ---- Helper to Move Between Stages ---- #
def go_to_stage(stage_name, key, value=None):
    if value:
        st.session_state.flow_data[key] = value
    st.session_state.stage = stage_name

# ---- Stage 1: Financial Priority ---- #
if st.session_state_
