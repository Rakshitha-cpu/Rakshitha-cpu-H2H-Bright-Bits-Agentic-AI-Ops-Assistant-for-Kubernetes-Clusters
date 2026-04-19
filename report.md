# One-Page Write-Up

## What Worked
- Groq API with llama-3.3-70b worked well
- Conversation memory worked for follow-up questions
- Streamlit UI looks professional
- Fault injection created realistic scenarios
- Agent correctly identified CrashLoopBackOff and Pending pods

## What Didn't Work
- Anthropic API required paid credits
- Gemini free tier quota ran out quickly
- Token limits required trimming kubectl output
- Local LLMs via Ollama too slow on limited RAM

## How It Scales to 200+ Services
1. Vector Search over pod metadata
2. One agent per namespace running in parallel
3. Cache kubectl results for 30 seconds
4. Only trigger agent when alerts fire
5. Read-only RBAC service account for safety
