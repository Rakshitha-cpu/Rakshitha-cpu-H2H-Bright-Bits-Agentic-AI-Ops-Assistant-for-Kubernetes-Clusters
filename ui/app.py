import streamlit as st
import sys
import os

sys.path.append(os.path.expanduser('~/Rakshitha-cpu-H2H-Bright-Bits-Agentic-AI-Ops-Assistant-for-Kubernetes-Clusters/agent'))
from agent import run_agent

st.set_page_config(
    page_title="K8s AI Assistant",
    page_icon="☸️",
    layout="wide"
)

st.title("☸️ K8s AI Diagnostic Assistant")
st.caption("Ask me anything about your Kubernetes cluster")

if "history" not in st.session_state:
    st.session_state.history = []
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("e.g. Which pods are crashing and why?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing cluster..."):
            response = run_agent(prompt, st.session_state.history)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
