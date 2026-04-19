bashcat > ~/Rakshitha-cpu-H2H-Bright-Bits-Agentic-AI-Ops-Assistant-for-Kubernetes-Clusters/README.md << 'EOF'
# ☸️ Agentic AI Ops Assistant for Kubernetes Clusters

> An AI-powered web assistant that monitors, diagnoses, and recommends fixes for a local Kubernetes cluster using natural language queries.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.35-blue)
![Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203.3-orange)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![Minikube](https://img.shields.io/badge/Cluster-Minikube-green)

---

## 📌 Project Overview

This project builds an AI-powered assistant that:
- Accepts natural language queries about your Kubernetes cluster
- Autonomously runs kubectl commands to gather data
- Reasons over the data using an LLM
- Provides root-cause analysis and exact fix commands
- Remembers conversation context for follow-up questions

---

## 🏗️ Architecture
User (Natural Language)
↓
Streamlit Web UI
↓
AI Agent (Groq + Llama 3.3-70b)
↓
kubectl Tool Calls
↓
Minikube Cluster
(Google Online Boutique - 11 Microservices)
↓
Root Cause Summary + Fix Commands

---

## 🧰 Tech Stack

| Component | Technology |
|-----------|------------|
| Local Cluster | Minikube v1.38 |
| Microservices | Google Online Boutique (11 services) |
| AI Model | Llama 3.3-70b-versatile via Groq API |
| Agent Framework | Custom ReAct Loop |
| Web UI | Streamlit |
| Language | Python 3.12 |
| OS | Ubuntu 24.04 (WSL2) |

---

## 🤖 Model Choice Rationale

**Groq API with llama-3.3-70b-versatile** was chosen because:
- ✅ Completely free with no credit card required
- ✅ Fast inference (low latency responses)
- ✅ Strong reasoning ability for Kubernetes diagnosis
- ✅ Good at understanding kubectl command outputs
- ✅ Handles multi-turn conversation well

**Alternatives considered:**
- Anthropic Claude — requires paid credits
- Google Gemini — free tier quota ran out quickly
- Ollama (local LLM) — too slow on limited RAM (8GB)

---

## 💥 Injected Faults

4 deliberate faults were injected for AI diagnosis:

| Fault | Pod/Service | Reason | Symptom |
|-------|-------------|--------|---------|
| CrashLoopBackOff | crashloop-app | Container exits with code 1 | Restarts repeatedly |
| Pending Pod | pending-pod | Requests 100GB RAM | Never gets scheduled |
| Broken Service | broken-service | Wrong selector label | 0 endpoints, no traffic |
| OOMKilled | oom-pod | Memory limit too low (50Mi) | Gets killed by OS |

---

## 🚀 Setup Instructions

### Prerequisites
- Windows 11 with WSL2 + Ubuntu 24.04
- Docker installed and running
- At least 4 CPU cores and 8GB RAM
- Groq API key (free at console.groq.com)

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

## 💬 5 Diagnostic Conversations

### Conversation 1 — Pod Status
You: Which pods are not running and why?
AI:  Diagnosed crashloop-app (CrashLoopBackOff) and
pending-pod (Insufficient resources)
Fix: kubectl patch deployment crashloop-app...

### Conversation 2 — Pending Pod
You: Why is pending-pod stuck?
AI:  Pod requests 100Gi RAM but node only has 3Gi
Fix: Reduce memory request to 128Mi

### Conversation 3 — Service Diagnosis
You: Is broken-service routing traffic correctly?
AI:  Service has 0 endpoints. Selector points to
nonexistent-app which has no matching pods
Fix: Update selector to match real pod labels

### Conversation 4 — Namespace Follow-up
You: What about the staging namespace?
AI:  No pods running in staging namespace
Cluster only has workloads in default namespace

### Conversation 5 — Fix All Issues
You: How do I fix all the issues you found?
AI:  1. Fix crashloop: kubectl patch deployment...
2. Fix pending: kubectl edit pod pending-pod...
3. Fix service: kubectl edit service broken-service...

---

## 🧠 Agent Features

### Natural Language to kubectl
"Which pods are crashing?"
↓
kubectl get pods
kubectl describe pod crashloop-app
kubectl get events
↓
Root cause analysis + fix commands

### Conversation Memory
Agent remembers previous questions so follow-up
questions work naturally:
You: Which pods are broken?
You: Why is that happening?      ← remembers context
You: What about staging?         ← remembers context
You: How do I fix everything?    ← summarizes all issues

### Full Transparency Logging
Every tool call is logged in logs/agent.log:
2026-04-19 10:23:01 - USER QUERY: Which pods are not running?
2026-04-19 10:23:01 - TOOL CALL: kubectl get pods
2026-04-19 10:23:02 - TOOL RESULT: NAME STATUS...
2026-04-19 10:23:03 - FINAL ANSWER: Diagnosed 2 issues...

---

## 📁 Project Structure
├── agent/
│   └── agent.py          # AI agent with ReAct loop
├── cluster/
│   └── setup.sh          # Cluster setup script
├── faults/
│   └── faults.yaml       # 4 injected fault definitions
├── logs/
│   └── agent.log         # Tool call transparency logs
├── ui/
│   └── app.py            # Streamlit web interface
├── README.md             # This file
├── report.md             # One-page write-up
└── requirements.txt      # Python dependencies

---

## 📊 How It Scales to 200+ Services

| Challenge | Solution |
|-----------|----------|
| Too many pods to scan | Vector search over pod metadata |
| Single agent bottleneck | One agent per namespace |
| Slow kubectl calls | Cache results for 30 seconds |
| Too many alerts | Only trigger on alert events |
| Security risk | Read-only RBAC service account |

### Production Architecture
AlertManager
→ Agent Router
→ Namespace Agent (frontend)
→ Namespace Agent (backend)
→ Namespace Agent (data)
↓
kubectl (read-only)
↓
Root Cause Summary
↓
Slack / PagerDuty

---

## 👩‍💻 Author

**Rakshitha**
GitHub: [@Rakshitha-cpu](https://github.com/Rakshitha-cpu)

---

## 📄 License

MIT License — free to use and modify
EOF
