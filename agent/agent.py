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
When asked a question about the cluster:
1. Run kubectl commands to gather data
2. Analyze the output
3. Explain what is wrong
4. Give exact commands to fix it"""

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
        logger.info(f"TOOL RESULT: {output[:300]}")
        return output
    except Exception as e:
        return f"Error: {str(e)}"

def run_agent(user_query, conversation_history):
    logger.info(f"USER QUERY: {user_query}")

    plan_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Question: {user_query}\n\nList the kubectl commands needed to answer this. One command per line, without the kubectl prefix."}
    ]

    plan_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=plan_messages,
        max_tokens=500
    )

    commands_text = plan_response.choices[0].message.content.strip()
    print(f"\n📋 Planning:\n{commands_text}\n")

    results = {}
    for line in commands_text.split('\n'):
        line = line.strip().replace('kubectl ', '').replace('`', '').strip()
        if line and not line.startswith('#') and len(line) > 3:
            print(f"\n🔧 Running: kubectl {line}")
            output = run_kubectl(line)
            results[line] = output
            print(f"📋 Result: {output[:200]}")

    context = f"Question: {user_query}\n\nkubectl results:\n"
    for cmd, output in results.items():
        context += f"\nkubectl {cmd}:\n{output}\n"

    if conversation_history:
        context += "\nPrevious conversation:\n"
        for role, msg in conversation_history[-4:]:
            context += f"{role}: {msg}\n"

    context += "\nNow give a clear diagnosis and exact fix commands."

    final_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": context}
    ]

    final_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=final_messages,
        max_tokens=1000
    )

    answer = final_response.choices[0].message.content
    conversation_history.append(("User", user_query))
    conversation_history.append(("Assistant", answer))
    logger.info(f"FINAL ANSWER: {answer[:300]}")
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
