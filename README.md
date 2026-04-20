# ☸️ Agentic AI Ops Assistant for Kubernetes Clusters

> AI-powered Kubernetes diagnostics using natural language — just ask, it diagnoses and fixes.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.35-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3-F55036?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

## 🚨 Problem Statement

Managing Kubernetes clusters is complex and requires deep expertise.
When pods crash, services break, or resources run out — engineers
spend hours manually running kubectl commands, reading logs, and
searching documentation to find the root cause.

**The problem:**
- Kubernetes errors are cryptic and hard to understand
- Debugging requires running 10+ commands manually
- New engineers don't know where to start
- Downtime costs money every minute

---

## 💡 Proposed Solution

An AI-powered assistant that:
- Accepts plain English questions about your cluster
- Automatically runs the right kubectl commands
- Reasons over the output using an LLM
- Returns a clear root-cause explanation + exact fix commands
- Remembers conversation context for follow-up questions

**What makes it unique:**
- No Kubernetes expertise needed — just ask in plain English
- Fully autonomous — no manual command running
- Conversation memory — follow-up questions work naturally
- Complete transparency — every tool call is logged

---

## ✨ Features

- 🗣️ Natural language queries — ask in plain English
- ⚙️ Auto kubectl execution — agent runs commands itself
- 🧠 Root cause analysis — explains WHY things break
- 🔧 Exact fix commands — tells you exactly what to run
- 💬 Conversation memory — follow-up questions work
- 📝 Full transparency logging — every step logged
- 🖥️ Beautiful web UI — dark theme dashboard
- 🔴 Fault injection — 4 real faults for testing
- 📊 Live cluster status — pod counts in sidebar
- ⚡ Quick diagnose buttons — one click diagnosis

---

## 🏗️ Architecture

```mermaid
flowchart TD
    A[👤 User — Natural Language Query] --> B[🖥️ Streamlit Web UI]
    B --> C[🧠 AI Agent — Groq + Llama 3.3]
    C --> D[⚙️ kubectl Tool Calls]
    D --> E[☸️ Minikube Cluster]
    E --> C
    C --> F[📋 Root Cause + Fix Commands]
    F --> B
    C --> G[📝 logs/agent.log]

    style A fill:#1e3a5f,color:#93c5fd
    style B fill:#064e3b,color:#6ee7b7
    style C fill:#1e1b4b,color:#a5b4fc
    style D fill:#451a03,color:#fcd34d
    style E fill:#1e3a5f,color:#93c5fd
    style F fill:#064e3b,color:#6ee7b7
    style G fill:#3b0764,color:#d8b4fe
```

---

## 🧰 Tech Stack

| Component | Technology | Why |
|-----------|------------|-----|
| Local Cluster | Minikube v1.38 | Easy local K8s |
| Microservices | Google Online Boutique | Real 11-service app |
| AI Model | Llama 3.3-70b via Groq | Free and fast |
| Agent Framework | Custom ReAct Loop | Full control |
| Web UI | Streamlit | Professional UI |
| Language | Python 3.12 | Best AI support |
| Platform | Ubuntu 24.04 WSL2 | Linux on Windows |

---

## 🤖 Model Choice

**Groq API + llama-3.3-70b-versatile** chosen because:
- ✅ Completely FREE
- ✅ Fast inference
- ✅ Strong Kubernetes reasoning
- ✅ Multi-turn conversation support

| Model | Reason Rejected |
|-------|----------------|
| Anthropic Claude | Requires paid credits |
| Google Gemini | Free quota ran out |
| Ollama local | Too slow on 8GB RAM |

---

## 💥 Injected Faults

| Fault Type | Resource | Root Cause | Symptom |
|------------|----------|------------|---------|
| CrashLoopBackOff | crashloop-app | Exit code 1 | Restarts forever |
| Pending Pod | pending-pod | Requests 100Gi RAM | Never scheduled |
| Broken Service | broken-service | Wrong selector | 0 endpoints |
| OOMKilled | oom-pod | Memory limit 50Mi | Killed by OS |

---

## 🚀 Setup Instructions

### Prerequisites
- Windows 11 with WSL2 + Ubuntu 24.04
- Docker installed
- 4 CPU cores, 8GB RAM
- Groq API key — free at console.groq.com

### Step 1 — Start Docker
```bash
sudo dockerd > /dev/null 2>&1 &
```

### Step 2 — Start Minikube
```bash
minikube start --cpus=4 --memory=3000 --driver=docker
```

### Step 3 — Deploy Microservices
```bash
git clone https://github.com/GoogleCloudPlatform/microservices-demo.git
kubectl apply -f microservices-demo/release/kubernetes-manifests.yaml
```

### Step 4 — Inject Faults
```bash
kubectl apply -f faults/faults.yaml
```

### Step 5 — Install Dependencies
```bash
pip3 install -r requirements.txt --break-system-packages
```

### Step 6 — Set API Key
```bash
export GROQ_API_KEY="your-groq-key-here"
```

### Step 7 — Run Web UI
```bash
python3 -m streamlit run ui/app.py
```

### Step 8 — Open Browser
http://localhost:8501

---

## 🎥 Demo Video

[▶️ Watch Demo on YouTube](#) ← add your link here

---

## 📸 Screenshots

### Web UI Dashboard
![Dashboard](screenshots/dashboard.png)

### AI Diagnosis in Action
![Diagnosis](screenshots/diagnosis.png)

### Cluster Status Sidebar
![Sidebar](screenshots/sidebar.png)

---

## 💬 5 Diagnostic Conversations

### 1️⃣ Find Broken Pods
You: Which pods are not running and why?
AI:  crashloop-app → CrashLoopBackOff (exit code 1)
pending-pod   → Pending (needs 100Gi RAM)

### 2️⃣ Follow-up Memory Test
You: Why is that happening?
AI:  Remembers context from Question 1 and explains
root causes of those specific pods

### 3️⃣ Service Diagnosis
You: Is broken-service routing traffic correctly?
AI:  No. 0 endpoints. Wrong selector label.
Fix: kubectl edit service broken-service

### 4️⃣ Namespace Follow-up
You: What about the staging namespace?
AI:  staging exists but has no pods running.

### 5️⃣ Fix Everything
You: How do I fix all the issues?
AI:  Complete fix guide for all 3 issues found

---

## 📝 Transparency Logging
2026-04-19 10:23:01 - USER QUERY: Which pods are not running?
2026-04-19 10:23:01 - TOOL CALL: kubectl get pods
2026-04-19 10:23:02 - TOOL RESULT: NAME READY STATUS...
2026-04-19 10:23:03 - FINAL ANSWER: Two pods not running...

---
## Project Structure

```text
├── agent/
│   └── agent.py            # AI agent ReAct loop
├── cluster/
│   └── setup.sh            # Cluster setup script
├── faults/
│   └── faults.yaml         # Contains 4 injected faults
├── logs/
│   └── agent.log           # Transparency and execution logs
├── ui/
│   └── app.py              # Streamlit web interface
├── README.md               # Project documentation
├── report.md               # One-page project write-up
└── requirements.txt        # Python dependencies
```
---

## 📈 Scaling to 200+ Services

| Challenge | Solution |
|-----------|----------|
| Too many pods | Vector DB search |
| Single bottleneck | One agent per namespace |
| Slow kubectl | Cache 30 seconds |
| Alert overload | Trigger on alerts only |
| Security | Read-only RBAC |

```mermaid
flowchart TD
    A[🚨 Alert Manager] --> B[🔀 Agent Router]
    B --> C[🤖 Agent frontend]
    B --> D[🤖 Agent backend]
    B --> E[🤖 Agent data]
    C --> F[⚙️ kubectl read-only]
    D --> F
    E --> F
    F --> G[📋 Root Cause]
    G --> H[📣 Slack/PagerDuty]

    style A fill:#7f1d1d,color:#fca5a5
    style B fill:#1e3a5f,color:#93c5fd
    style C fill:#064e3b,color:#6ee7b7
    style D fill:#064e3b,color:#6ee7b7
    style E fill:#064e3b,color:#6ee7b7
    style F fill:#451a03,color:#fcd34d
    style G fill:#1e1b4b,color:#a5b4fc
    style H fill:#064e3b,color:#6ee7b7
```

---

## 👥 Team Members

| Name | Role | GitHub |
|------|------|--------|
| Rakshitha R | AI Agent + Backend | [@Rakshitha-cpu](https://github.com/Rakshitha-cpu) |
| Poojary Nisarga Arun | Frontend + DevOps | [https://github.com/Nisarga582] |

---

## 🌐 Deployed Link

[Live Demo →](#) ← add your deployed URL here

---

## 📄 License

MIT License — H2H Bright Bits Hackathon 2026
