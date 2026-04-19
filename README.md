# ☸️ Agentic AI Ops Assistant for Kubernetes Clusters

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.35-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Minikube](https://img.shields.io/badge/Minikube-1.38-F5A623?style=for-the-badge&logo=kubernetes&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3-F55036?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**An AI-powered web assistant that monitors, diagnoses, and recommends fixes for a local Kubernetes cluster using natural language.**

[Features](#-features) • [Architecture](#-architecture) • [Setup](#-setup-instructions) • [Demo](#-demo-conversations) • [Model Choice](#-model-choice)

</div>

---

## 📌 Project Overview

This project is a submission for **H2H Bright Bits Hackathon** under the AI/DevOps category.

It builds an intelligent Kubernetes diagnostic assistant that:
- 🔍 Accepts natural language queries about your cluster
- ⚙️ Autonomously runs kubectl commands to gather data
- 🧠 Reasons over the output using an LLM
- 🔧 Provides root-cause analysis and exact fix commands
- 💬 Remembers conversation context for follow-up questions
- 📝 Logs every tool call for full transparency

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🗣️ Natural Language | Ask questions in plain English |
| ⚙️ Auto kubectl | Agent runs commands automatically |
| 🧠 Root Cause Analysis | Explains WHY things are broken |
| 🔧 Fix Commands | Gives exact commands to fix issues |
| 💬 Conversation Memory | Follow-up questions work naturally |
| 📝 Full Logging | Every tool call logged transparently |
| 🖥️ Web UI | Beautiful Streamlit dashboard |
| 🔴 Fault Injection | 4 real faults for realistic testing |

---

## 🏗️ Architecture
┌─────────────────────────────────────────────────────────┐
│                     USER INTERFACE                       │
│              Streamlit Web App (port 8501)               │
└─────────────────────────┬───────────────────────────────┘
│ Natural Language Query
▼
┌─────────────────────────────────────────────────────────┐
│                     AI AGENT LAYER                       │
│         Groq API + Llama 3.3-70b-versatile               │
│                                                          │
│   1. Understands the question                            │
│   2. Decides which kubectl commands to run               │
│   3. Analyzes the output                                 │
│   4. Generates root cause + fix                          │
└─────────────────────────┬───────────────────────────────┘
│ kubectl commands
▼
┌─────────────────────────────────────────────────────────┐
│                   KUBERNETES LAYER                       │
│                 Minikube Cluster                         │
│                                                          │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│   │  frontend   │  │ cartservice │  │  checkout   │    │
│   └─────────────┘  └─────────────┘  └─────────────┘    │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│   │ crashloop   │  │ pending-pod │  │broken-svc   │    │
│   │ (FAULT 1)   │  │ (FAULT 2)   │  │ (FAULT 3)   │    │
│   └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────┬───────────────────────────────┘
│ Results
▼
┌─────────────────────────────────────────────────────────┐
│                    LOGGING LAYER                         │
│              logs/agent.log                              │
│   Logs every tool call, query, and final answer          │
└─────────────────────────────────────────────────────────┘

---

## 🧰 Tech Stack

| Component | Technology | Why |
|-----------|------------|-----|
| Local Cluster | Minikube v1.38 | Easy local K8s setup |
| Microservices | Google Online Boutique | Real 11-service app |
| AI Model | Llama 3.3-70b via Groq | Free, fast, accurate |
| Agent Framework | Custom ReAct Loop | Full control |
| Web UI | Streamlit | Fast to build, looks great |
| Language | Python 3.12 | Best AI/DevOps support |
| Platform | Ubuntu 24.04 WSL2 | Linux tools on Windows |

---

## 🤖 Model Choice

**Groq API + llama-3.3-70b-versatile** was chosen because:
✅ Completely FREE — no credit card needed
✅ Very fast inference — low latency
✅ Strong reasoning over kubectl output
✅ Handles multi-turn conversation well
✅ Understands Kubernetes concepts natively

**Alternatives tested and rejected:**

| Model | Reason Rejected |
|-------|----------------|
| Anthropic Claude | Requires paid credits ($5 min) |
| Google Gemini | Free quota ran out in minutes |
| Ollama (local) | Too slow on 8GB RAM |
| GPT-4 | Requires paid OpenAI credits |

---

## 💥 Injected Faults

4 deliberate faults were created for AI diagnosis testing:
┌──────────────────┬──────────────────┬──────────────────────┬─────────────────────┐
│ Fault Type       │ Resource         │ Root Cause           │ Symptom             │
├──────────────────┼──────────────────┼──────────────────────┼─────────────────────┤
│ CrashLoopBackOff │ crashloop-app    │ Exit code 1          │ Restarts forever    │
│ Pending Pod      │ pending-pod      │ Requests 100Gi RAM   │ Never scheduled     │
│ Broken Service   │ broken-service   │ Wrong selector label │ 0 endpoints         │
│ OOMKilled        │ oom-pod          │ Memory limit 50Mi    │ Killed by OS        │
└──────────────────┴──────────────────┴──────────────────────┴─────────────────────┘

---

## 🚀 Setup Instructions

### Prerequisites

Windows 11 with WSL2 + Ubuntu 24.04
Docker installed
4+ CPU cores, 8GB RAM
Groq API key (free at console.groq.com)


### Step 1 — Start Docker
```bash
sudo dockerd > /dev/null 2>&1 &
```

### Step 2 — Start Minikube
```bash
minikube start --cpus=4 --memory=3000 --driver=docker
```

### Step 3 — Deploy Online Boutique
```bash
git clone https://github.com/GoogleCloudPlatform/microservices-demo.git
kubectl apply -f microservices-demo/release/kubernetes-manifests.yaml
```

### Step 4 — Create Staging Namespace
```bash
kubectl create namespace staging
```

### Step 5 — Inject Faults
```bash
kubectl apply -f faults/faults.yaml
```

### Step 6 — Install Dependencies
```bash
pip3 install -r requirements.txt --break-system-packages
```

### Step 7 — Set API Key
```bash
export GROQ_API_KEY="your-groq-key-here"
```

### Step 8 — Run Web UI
```bash
python3 -m streamlit run ui/app.py
```

### Step 9 — Open Browser
http://localhost:8501

---

## 💬 Demo Conversations

### Conversation 1 — Find Broken Pods
You: Which pods are not running and why?
AI:  Two pods are not running:
 1. crashloop-app — CrashLoopBackOff
    Container command exits with code 1
    Fix: kubectl patch deployment crashloop-app -p
    '{"spec":{"template":{"spec":{"containers":
    [{"name":"crashloop-app","command":
    ["tail","-f","/dev/null"]}]}}}}'

 2. pending-pod — Pending
    Requests 100Gi RAM but node only has 3Gi
    Fix: kubectl edit pod pending-pod
    Change memory request to 128Mi

### Conversation 2 — Follow-up Question (Memory Test)
You: Why is that happening?
AI:  Based on what we found earlier:
crashloop-app crashes because the container
command intentionally exits with error code 1.
pending-pod is stuck because no node in the
cluster has 100GB of RAM available.

### Conversation 3 — Service Diagnosis
You: Is broken-service routing traffic correctly?
AI:  No. broken-service has 0 endpoints.
The service selector is set to:
app: nonexistent-app
But no pod has this label.
Fix: kubectl edit service broken-service
Change selector to match an actual pod label.

### Conversation 4 — Namespace Follow-up
You: What about the staging namespace?
AI:  The staging namespace exists but has no pods.
All workloads are running in the default namespace.
To deploy to staging:
kubectl apply -f manifests/ -n staging

### Conversation 5 — Fix Everything
You: How do I fix all the issues you found?
AI:  Here are fixes for all 3 issues found:
 1. Fix crashloop-app:
    kubectl patch deployment crashloop-app...

 2. Fix pending-pod:
    kubectl edit pod pending-pod
    Change memory: 100Gi → 128Mi

 3. Fix broken-service:
    kubectl edit service broken-service
    Change selector to correct label

---

## 🧠 How the Agent Works
User asks: "Which pods are crashing?"
│
▼
Agent plans kubectl commands:
- kubectl get pods
- kubectl describe pod <failing-pod>
- kubectl get events
│
▼
Executes each command
Captures output
Logs everything to agent.log
│
▼
Sends all output to Llama 3.3
LLM reasons over the data
│
▼
Returns: Root cause + exact fix commands

---

## 📊 Conversation Memory

Agent remembers all previous questions:
Turn 1: "Which pods are broken?"
→ Agent finds crashloop-app and pending-pod
Turn 2: "Why is that happening?"
→ Agent remembers Turn 1 context
→ Explains root causes of THOSE specific pods
Turn 3: "What about staging?"
→ Agent checks staging namespace
→ Remembers all previous context
Turn 4: "How do I fix everything?"
→ Agent summarizes ALL issues from Turn 1-3
→ Gives one complete fix guide

---

## 📝 Transparency Logging

Every action is logged in `logs/agent.log`:
2026-04-19 10:23:01 - USER QUERY: Which pods are not running?
2026-04-19 10:23:01 - TOOL CALL: kubectl get pods
2026-04-19 10:23:02 - TOOL RESULT: NAME READY STATUS...
2026-04-19 10:23:02 - TOOL CALL: kubectl get events
2026-04-19 10:23:03 - TOOL RESULT: LAST SEEN TYPE...
2026-04-19 10:23:04 - FINAL ANSWER: Two pods are not running...

---

## 📁 Project Structure
Rakshitha-cpu-H2H-Bright-Bits-Agentic-AI-Ops-Assistant/
│
├── 📁 agent/
│   └── agent.py              # AI agent with ReAct loop
│
├── 📁 cluster/
│   └── setup.sh              # One-click cluster setup
│
├── 📁 faults/
│   └── faults.yaml           # 4 injected fault definitions
│
├── 📁 logs/
│   └── agent.log             # Transparency logs
│
├── 📁 ui/
│   └── app.py                # Streamlit web dashboard
│
├── README.md                 # This documentation
├── report.md                 # One-page write-up
└── requirements.txt          # Python dependencies

---

## 📈 Scaling to 200+ Services

| Challenge | Solution |
|-----------|----------|
| Too many pods to scan | Vector DB for pod metadata search |
| Single agent bottleneck | One agent per namespace |
| Slow kubectl calls | Cache results 30 seconds |
| Alert overload | Trigger only on real alerts |
| Security risk | Read-only RBAC service account |
| High token usage | Summarize before sending to LLM |

### Production Architecture
┌─────────────────────────────────────────────┐
│              Alert Manager                   │
│     (fires when pod crashes or is pending)   │
└─────────────────┬───────────────────────────┘
│
▼
┌─────────────────────────────────────────────┐
│              Agent Router                    │
│     (decides which namespace agent to use)   │
└──────┬──────────────┬────────────────┬───────┘
│              │                │
▼              ▼                ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│  Agent     │ │  Agent     │ │  Agent     │
│ (frontend) │ │ (backend)  │ │  (data)    │
└─────┬──────┘ └─────┬──────┘ └─────┬──────┘
│              │              │
└──────────────┼──────────────┘
│
▼
kubectl (read-only)
│
▼
Root Cause Summary
│
▼
Slack / PagerDuty Alert

---

## 👩‍💻 Author

**Rakshitha R**
- GitHub: [@Rakshitha-cpu](https://github.com/Rakshitha-cpu)
- Hackathon: H2H Bright Bits — AI/DevOps Track

---

## 📄 License

MIT License — free to use, modify and distribute.
