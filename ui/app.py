
import streamlit as st
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agent import run_agent, run_kubectl, get_last_commands

st.set_page_config(
    page_title="K8s AI Ops Assistant",
    page_icon="☸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"], .stApp {
    background: linear-gradient(180deg, #07111d 0%, #050b14 100%) !important;
    color: #e8f1fb !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

section[data-testid="stSidebar"] {
    background: #08111c !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}

.block-container {
    max-width: 1450px !important;
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}

h1, h2, h3, h4, h5, h6, p, span, div, label {
    color: #e8f1fb !important;
}

.hero {
    background: linear-gradient(180deg, rgba(12,24,40,0.95), rgba(9,18,31,0.98));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 22px 24px;
    margin-bottom: 18px;
}

.hero-title {
    font-size: 2.3rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 6px;
}

.hero-sub {
    color: #9fb7cf !important;
    font-size: 1rem;
}

.soft-card {
    background: linear-gradient(180deg, rgba(12,24,40,0.95), rgba(9,18,31,0.98));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 14px 16px;
    margin-bottom: 14px;
}

.section-label {
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 800;
    color: #9fb7cf !important;
    margin-bottom: 10px;
}

.metric-wrap {
    background: linear-gradient(180deg, rgba(12,24,40,0.95), rgba(9,18,31,0.98));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 16px 18px;
    min-height: 132px;
}

.metric-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #9fb7cf !important;
    font-weight: 800;
}

.metric-value {
    font-size: 2rem;
    font-weight: 800;
    margin-top: 8px;
}

.metric-sub {
    color: #b9cde2 !important;
    margin-top: 8px;
    font-size: 0.92rem;
}

.badge-live {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(20,83,45,0.7);
    color: #86efac !important;
    border: 1px solid rgba(34,197,94,0.3);
    font-size: 0.82rem;
    font-weight: 800;
}

.status-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.92rem;
}

.status-row:last-child {
    border-bottom: none;
}

.badge-green, .badge-red, .badge-yellow, .badge-blue {
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 0.76rem;
    font-weight: 800;
}

.badge-green { background: rgba(20,83,45,0.72); color: #86efac !important; }
.badge-red { background: rgba(127,29,29,0.72); color: #fca5a5 !important; }
.badge-yellow { background: rgba(120,53,15,0.72); color: #fcd34d !important; }
.badge-blue { background: rgba(30,64,175,0.72); color: #bfdbfe !important; }

.welcome-card {
    background: linear-gradient(180deg, rgba(12,24,40,0.95), rgba(9,18,31,0.98));
    border: 1px solid rgba(56,189,248,0.22);
    border-left: 4px solid #38bdf8;
    border-radius: 18px;
    padding: 18px 20px;
    margin-bottom: 14px;
}

.welcome-title {
    font-size: 1.06rem;
    font-weight: 800;
    margin-bottom: 8px;
}

.welcome-sub {
    color: #a6bfd8 !important;
    font-size: 0.93rem;
    line-height: 1.7;
}

.chat-card {
    background: linear-gradient(180deg, rgba(12,24,40,0.95), rgba(9,18,31,0.98));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 16px 18px;
    margin-bottom: 14px;
}

.chat-label {
    font-size: 0.82rem;
    color: #9fb7cf !important;
    margin-bottom: 8px;
    font-weight: 700;
}

.chat-value {
    font-size: 1rem;
    line-height: 1.7;
    white-space: pre-wrap;
}

.answer-box {
    background: linear-gradient(180deg, rgba(12,24,40,0.95), rgba(9,18,31,0.98));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
}

.answer-section {
    margin-bottom: 16px;
}

.answer-section:last-child {
    margin-bottom: 0;
}

.answer-title {
    font-size: 0.95rem;
    font-weight: 800;
    margin-bottom: 8px;
    letter-spacing: 0.04em;
}

.answer-evidence { color: #38bdf8 !important; }
.answer-root { color: #f87171 !important; }
.answer-fix { color: #4ade80 !important; }
.answer-verify { color: #60a5fa !important; }

.fault-item {
    padding: 9px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.92rem;
}

.fault-item:last-child {
    border-bottom: none;
}

.stButton > button {
    width: 100% !important;
    border-radius: 12px !important;
    background: #0d1b2a !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #e8f1fb !important;
    font-weight: 600 !important;
    padding: 0.8rem 0.95rem !important;
    text-align: left !important;
}

.stButton > button:hover {
    border-color: rgba(56,189,248,0.45) !important;
    color: #7dd3fc !important;
}

[data-testid="stChatInputContainer"] {
    background: #0d1b2a !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
}

[data-testid="stChatInputContainer"] textarea {
    color: #e8f1fb !important;
    background: transparent !important;
}

[data-testid="stCodeBlock"] {
    border-radius: 12px !important;
    overflow: hidden !important;
}

[data-testid="stCodeBlock"] pre {
    background: #0b1220 !important;
    color: #dbeafe !important;
}

[data-testid="stExpander"] {
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    background: rgba(10, 19, 32, 0.75) !important;
}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_q" not in st.session_state:
    st.session_state.quick_q = None


def safe_get_pods():
    try:
        return run_kubectl("get pods")
    except Exception:
        return ""


def summarize_cluster():
    pods_output = safe_get_pods()

    if not pods_output.strip():
        return {"running": "-", "error": "-", "pending": "-", "total": "-"}

    lowered = pods_output.lower()
    if (
        "connection refused" in lowered
        or "unable to connect" in lowered
        or "server misbehaving" in lowered
        or "error from server" in lowered
        or "no such host" in lowered
    ):
        return {"running": "-", "error": "-", "pending": "-", "total": "-"}

    lines = [l for l in pods_output.strip().split("\n")[1:] if l.strip()]

    running = sum(1 for l in lines if "Running" in l)
    error = sum(
        1
        for l in lines
        if "Error" in l or "CrashLoopBackOff" in l or "ImagePullBackOff" in l or "ErrImagePull" in l
    )
    pending = sum(1 for l in lines if "Pending" in l)
    total = len(lines)

    return {
        "running": running,
        "error": error,
        "pending": pending,
        "total": total,
    }


def split_sections(response: str):
    sections = {"EVIDENCE": [], "ROOT CAUSE": [], "FIX": [], "VERIFY": []}
    current = None
    for raw_line in response.splitlines():
        line = raw_line.strip()
        if line in sections:
            current = line
            continue
        if current is not None and line:
            if line.startswith("- "):
                line = line[2:]
            sections[current].append(line)
    return sections


def render_answer(response: str):
    if "\\n" in response:
        response = response.replace("\\n", "\n")

    if "ROOT CAUSE" not in response and "FIX" not in response and "VERIFY" not in response:
        st.markdown('<div class="answer-box">', unsafe_allow_html=True)
        for line in response.splitlines():
            if line.strip():
                st.markdown(f"- {line}")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    sections = split_sections(response)

    if not any(sections.values()):
        st.markdown('<div class="answer-box">', unsafe_allow_html=True)
        st.write(response)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.markdown('<div class="answer-box">', unsafe_allow_html=True)

    mapping = [
        ("EVIDENCE", "📌 EVIDENCE", "answer-evidence"),
        ("ROOT CAUSE", "🎯 ROOT CAUSE", "answer-root"),
        ("FIX", "🛠 FIX", "answer-fix"),
        ("VERIFY", "✅ VERIFY", "answer-verify"),
    ]

    for key, title, css_cls in mapping:
        st.markdown('<div class="answer-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="answer-title {css_cls}">{title}</div>', unsafe_allow_html=True)
        content = sections.get(key, [])
        if content:
            for item in content:
                st.markdown(f"- {item}")
        else:
            st.markdown("- —")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_commands():
    commands = get_last_commands()
    with st.expander("Commands Used", expanded=False):
        if commands:
            for cmd in commands:
                st.code(f"kubectl {cmd}", language="bash")
        else:
            st.write("No commands recorded.")


cluster = summarize_cluster()
if isinstance(cluster["error"], int) and isinstance(cluster["pending"], int):
    issue_count = cluster["error"] + cluster["pending"]
    issue_text = f"{issue_count} currently visible runtime issues found from live pod state."
else:
    issue_text = "Live cluster status unavailable. Check Docker, Minikube, and kubectl connectivity."

with st.sidebar:
    st.markdown("""
    <div class="soft-card">
        <div style="font-size:1.7rem;font-weight:800;">☸️ K8s AI Ops</div>
        <div style="color:#9fb7cf;font-size:0.92rem;">Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">System Status</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="soft-card">
        <div class="fault-item">• Minikube — Online</div>
        <div class="fault-item">• Groq LLM — Connected</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Cluster Health</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="soft-card">
        <div class="status-row"><span>Running</span><span class="badge-green">{cluster['running']}</span></div>
        <div class="status-row"><span>Error / Crash</span><span class="badge-red">{cluster['error']}</span></div>
        <div class="status-row"><span>Pending</span><span class="badge-yellow">{cluster['pending']}</span></div>
        <div class="status-row"><span>Total Pods</span><span class="badge-blue">{cluster['total']}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Quick Diagnose</div>', unsafe_allow_html=True)
    for q in [
        "Which pods are not running?",
        "Why is pending-pod stuck?",
        "Is broken-service working?",
        "What about staging namespace?",
        "How do I fix all issues?",
        "What commands did you use to diagnose this?"
    ]:
        if st.button(q, key=f"q_{q}"):
            st.session_state.quick_q = q

    st.markdown('<div class="section-label">Injected Faults</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="soft-card">
        <div class="fault-item">• CrashLoopBackOff</div>
        <div class="fault-item">• Pending Pod (100Gi)</div>
        <div class="fault-item">• Broken Service</div>
        <div class="fault-item">• OOMKilled Pod</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑 Clear Chat", key="clear"):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

top_left, top_right = st.columns([5, 1])
with top_left:
    st.markdown("""
    <div class="hero">
        <div class="hero-title">☸️ K8s AI Ops Assistant</div>
        <div class="hero-sub">Natural language Kubernetes diagnostics — powered by Llama 3.3 via Groq</div>
    </div>
    """, unsafe_allow_html=True)
with top_right:
    st.markdown("""
    <div style="padding-top:38px;text-align:right;">
        <span class="badge-live">● LIVE</span>
    </div>
    """, unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("""
    <div class="metric-wrap">
        <div class="metric-label">Services</div>
        <div class="metric-value">11</div>
        <div class="metric-sub">Online Boutique</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="metric-wrap">
        <div class="metric-label">Faults</div>
        <div class="metric-value">4</div>
        <div class="metric-sub">Injected</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="metric-wrap">
        <div class="metric-label">Namespaces</div>
        <div class="metric-value">2</div>
        <div class="metric-sub">default + staging</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown("""
    <div class="metric-wrap">
        <div class="metric-label">Model</div>
        <div class="metric-value">Llama 3.3</div>
        <div class="metric-sub">Groq Free</div>
    </div>
    """, unsafe_allow_html=True)

st.info(issue_text)

main_col, right_col = st.columns([3, 1.05], gap="large")

with right_col:
    st.markdown("""
    <div class="soft-card">
        <div class="section-label" style="margin-bottom:8px;">Project Status</div>
        <div class="fault-item">• 4 injected demo faults configured</div>
        <div class="fault-item">• Agentic kubectl diagnosis enabled</div>
        <div class="fault-item">• Commands transparency enabled</div>
        <div class="fault-item">• Conversation flow enabled</div>
    </div>
    """, unsafe_allow_html=True)

with main_col:
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-card">
            <div class="welcome-title">Ready to diagnose your cluster</div>
            <div class="welcome-sub">
                Ask anything in plain English. Try:
                <br><br>
                <em>"Which pods are not running and why?"</em><br>
                <em>"Is broken-service routing traffic correctly?"</em><br>
                <em>"How do I fix all the issues you found?"</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown('<div class="chat-card">', unsafe_allow_html=True)
            st.markdown('<div class="chat-label">You</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-value">{msg["content"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            render_answer(msg["content"])

    def handle_prompt(prompt_text: str):
        st.session_state.messages.append({"role": "user", "content": prompt_text})
        with st.spinner("Analyzing cluster..."):
            response = run_agent(prompt_text, st.session_state.history)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    if st.session_state.quick_q:
        prompt = st.session_state.quick_q
        st.session_state.quick_q = None
        handle_prompt(prompt)

    prompt = st.chat_input("Ask about your Kubernetes cluster...")
    if prompt:
        handle_prompt(prompt)

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
        render_commands()
