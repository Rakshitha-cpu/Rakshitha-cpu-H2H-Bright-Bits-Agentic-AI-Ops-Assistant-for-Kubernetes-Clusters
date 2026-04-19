import subprocess
import logging
import os
from groq import Groq

logging.basicConfig(
    filename=os.path.expanduser('~/Rakshitha-cpu-H2H-Bright-Bits-Agentic-AI-Ops-Assistant-for-Kubernetes-Clusters/logs/agent.log'),
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
logger = logging.getLogger()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a Kubernetes expert assistant.
You help diagnose and fix Kubernetes cluster problems.
You remember previous questions in the conversation.
Give short and clear diagnosis with exact fix commands."""

def run_kubectl(command):
    logger.info(f"TOOL CALL: kubectl {command}")
    try:
        result = subprocess.run(
            f"kubectl {command}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout or result.stderr
        logger.info(f"TOOL RESULT: {output[:100]}")
        return output[:100]
    except Exception as e:
        return f"Error: {str(e)}"

def get_cluster_data(query):
    """Get relevant kubectl data based on query"""
    data = ""

    # always get pods
    pods = run_kubectl("get pods")
    data += f"Pods:\n{pods[:200]}\n\n"

    # if question about namespace
    if "namespace" in query.lower() or "staging" in query.lower():
        ns_pods = run_kubectl("get pods -n staging")
        data += f"Staging pods:\n{ns_pods[:200]}\n\n"

    # if question about service
    if "service" in query.lower() or "routing" in query.lower() or "traffic" in query.lower():
        svc = run_kubectl("get endpoints")
        data += f"Endpoints:\n{svc[:200]}\n\n"

    # if question about pending
    if "pending" in query.lower() or "stuck" in query.lower():
        events = run_kubectl("get events --sort-by='.lastTimestamp'")
        data += f"Events:\n{events[:200]}\n\n"

    # if question about crash
    if "crash" in query.lower() or "error" in query.lower() or "fix" in query.lower():
        events = run_kubectl("get events --sort-by='.lastTimestamp'")
        data += f"Events:\n{events[:200]}\n\n"

    return data

def run_agent(user_query, conversation_history):
    logger.info(f"USER QUERY: {user_query}")

    # get cluster data
    cluster_data = get_cluster_data(user_query)

    # build messages with full conversation history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # add previous conversation
    for role, msg in conversation_history[-6:]:
        if role == "User":
            messages.append({"role": "user", "content": msg})
        else:
            messages.append({"role": "assistant", "content": msg})

    # add current question with cluster data
    current = f"Question: {user_query}\n\nCluster Data:\n{cluster_data}\n\nGive diagnosis and fix."
    messages.append({"role": "user", "content": current})

    logger.info(f"SENDING {len(messages)} messages to LLM")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=300
    )

    answer = response.choices[0].message.content

    # save to history
    conversation_history.append(("User", user_query))
    conversation_history.append(("Assistant", answer[:200]))

    logger.info(f"FINAL ANSWER: {answer[:200]}")
    return answer

if __name__ == "__main__":
    print("K8s AI Assistant Ready!")
    print("Type your question or 'quit' to exit\n")
    history = []
    while True:
        query = input("You: ").strip()
        if query.lower() == "quit":
            break
        if not query:
            continue
        print("\n⏳ Analyzing cluster...\n")
        answer = run_agent(query, history)
        print(f"\n🤖 Assistant: {answer}\n")
