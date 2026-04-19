import streamlit as st
import sys
import os

sys.path.append(os.path.expanduser('~/Rakshitha-cpu-H2H-Bright-Bits-Agentic-AI-Ops-Assistant-for-Kubernetes-Clusters/agent'))
from agent import run_agent, run_kubectl

st.set_page_config(
    page_title="K8s AI Ops Assistant",
    page_icon="☸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono&display=swap');

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: #0a0f1e !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

section[data-testid="stSidebar"] {
    background-color: #0d1526 !important;
    border-right: 1px solid #1e3a5f !important;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

.stApp * {
    color: #ffffff;
}

p, li, span, label, div {
    color: #e2e8f0 !important;
}

h1, h2, h3, h4 {
    color: #ffffff !important;
}

.hero {
    padding: 20px 0 10px 0;
}

.hero-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #ffffff !important;
    line-height: 1.2;
}

.hero-blue {
    color: #38bdf8 !important;
}

.hero-sub {
    color: #94a3b8 !important;
    font-size: 1rem;
    margin-top: 6px;
}

.divider {
    border: none;
    border-top: 1px solid #1e3a5f;
    margin: 16px 0;
}

.status-box {
    background: #111827;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 12px;
}

.status-title {
    color: #94a3b8 !important;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
    font-weight: 600;
}

.status-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 0;
    border-bottom: 1px solid #1e3a5f;
}

.status-row:last-child {
    border-bottom: none;
}

.status-label {
    color: #cbd5e1 !important;
    font-size: 0.85rem;
}

.badge-green {
    background: #064e3b;
    color: #6ee7b7 !important;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    border: 1px solid #065f46;
}

.badge-red {
    background: #450a0a;
    color: #fca5a5 !important;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    border: 1px solid #7f1d1d;
}

.badge-yellow {
    background: #451a03;
    color: #fcd34d !important;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    border: 1px solid #78350f;
}

.badge-white {
    color: #ffffff !important;
    font-weight: 700;
    font-size: 0.85rem;
}

.fault-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 0;
    font-size: 0.85rem;
    color: #cbd5e1 !important;
}

.dot-red { color: #f87171 !important; font-size: 18px; line-height: 1; }
.dot-yellow { color: #fbbf24 !important; font-size: 18px; line-height: 1; }

.welcome-card {
    background: #111827;
    border: 1px solid #1e3a5f;
    border-left: 4px solid #38bdf8;
    border-radius: 10px;
    padding: 20px 24px;
    margin: 12px 0;
}

.welcome-title {
    color: #38bdf8 !important;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 10px;
}

.welcome-example {
    color: #38bdf8 !important;
    font-size: 0.9rem;
    margin: 4px 0;
    font-style: italic;
}

.welcome-text {
    color: #94a3b8 !important;
    font-size: 0.9rem;
}

.stButton > button {
    background: #111827 !important;
    color: #e2e8f0 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    text-align: left !important;
    width: 100% !important;
    padding: 8px 12px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
}

.stButton > button:hover {
    border-color: #38bdf8 !important;
    color: #38bdf8 !important;
    background: #0d1f35 !important;
}

[data-testid="stMetricValue"] {
    color: #38bdf8 !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
}

[data-testid="stMetricDelta"] {
    color: #6ee7b7 !important;
}

[data-testid="stChatMessage"] {
    background: #111827 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 10px !important;
    padding: 12px !important;
    margin: 6px 0 !important;
}

[data-testid="stChatMessage"] p {
    color: #e2e8f0 !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
}

[data-testid="stChatMessage"] code {
    background: #0a0f1e !important;
    color: #38bdf8 !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
}

[data-testid="stChatInputContainer"] {
    background: #111827 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 10px !important;
}

[data-testid="stChatInputContainer"] textarea {
    color: #e2e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.stSpinner > div {
    border-top-color: #38bdf8 !important;
}

[data-testid="stSidebarContent"] .stMarkdown p {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick_q" not in st.session_state:
    st.session_state.quick_q = None

with st.sidebar:
    st.markdown("<p class='status-title'>⬤ System Status</p>", unsafe_allow_html=True)
    st.markdown("""
    <div class='status-box'>
        <div class='fault-item'>
            <span style='color:#6ee7b7;font-size:10px;'>⬤</span>
            <span style='color:#cbd5e1;'>Minikube — Online</span>
        </div>
        <div class='fault-item'>
            <span style='color:#6ee7b7;font-size:10px;'>⬤</span>
            <span style='color:#cbd5e1;'>Groq LLM — Connected</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p class='status-title'>📊 Cluster Health</p>", unsafe_allow_html=True)
    try:
        pods_output = run_kubectl("get pods")
        lines = pods_output.strip().split('\n')[1:]
        running = sum(1 for l in lines if 'Running' in l)
        error = sum(1 for l in lines if 'Error' in l or 'CrashLoop' in l)
        pending = sum(1 for l in lines if 'Pending' in l)
        total = len(lines)
        st.markdown(f"""
        <div class='status-box'>
            <div class='status-row'>
                <span class='status-label'>Running</span>
                <span class='badge-green'>{running}</span>
            </div>
            <div class='status-row'>
                <span class='status-label'>Error / Crash</span>
                <span class='badge-red'>{error}</span>
            </div>
            <div class='status-row'>
                <span class='status-label'>Pending</span>
                <span class='badge-yellow'>{pending}</span>
            </div>
            <div class='status-row'>
                <span class='status-label'>Total Pods</span>
                <span class='badge-white'>{total}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except:
        st.error("Cannot reach cluster")

    st.markdown("<p class='status-title'>💡 Quick Diagnose</p>", unsafe_allow_html=True)
    questions = [
        "Which pods are not running?",
        "Why is pending-pod stuck?",
        "Is broken-service working?",
        "What about staging namespace?",
        "How do I fix all issues?"
    ]
    for q in questions:
        if st.button(q, key=f"q_{q}"):
            st.session_state.quick_q = q

    st.markdown("<p class='status-title'>🔴 Injected Faults</p>", unsafe_allow_html=True)
    st.markdown("""
    <div class='status-box'>
        <div class='fault-item'><span class='dot-red'>●</span><span>CrashLoopBackOff</span></div>
        <div class='fault-item'><span class='dot-yellow'>●</span><span>Pending Pod (100Gi RAM)</span></div>
        <div class='fault-item'><span class='dot-red'>●</span><span>Broken Service Selector</span></div>
        <div class='fault-item'><span class='dot-red'>●</span><span>OOMKilled Pod</span></div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Conversation", key="clear"):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

st.markdown("""
<div class='hero'>
    <div class='hero-title'>☸️ K8s <span class='hero-blue'>AI Ops</span> Assistant</div>
    <div class='hero-sub'>Natural language Kubernetes diagnostics — powered by Llama 3.3 via Groq</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Cluster", value="Minikube", delta="Running")
with col2:
    st.metric(label="Services", value="11", delta="Online Boutique")
with col3:
    st.metric(label="Faults", value="4", delta="Injected")
with col4:
    st.metric(label="Model", value="Llama 3.3", delta="Groq Free")

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class='welcome-card'>
        <div class='welcome-title'>👋 Ready to diagnose your cluster</div>
        <p class='welcome-text'>Ask me anything in plain English. Try these:</p>
        <p class='welcome-example'>"Which pods are not running and why?"</p>
        <p class='welcome-example'>"Why is pending-pod stuck?"</p>
        <p class='welcome-example'>"How do I fix all the issues you found?"</p>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.session_state.quick_q:
    prompt = st.session_state.quick_q
    st.session_state.quick_q = None
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Analyzing cluster..."):
            response = run_agent(prompt, st.session_state.history)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

if prompt := st.chat_input("Ask about your Kubernetes cluster..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Analyzing cluster..."):
            response = run_agent(prompt, st.session_state.history)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
