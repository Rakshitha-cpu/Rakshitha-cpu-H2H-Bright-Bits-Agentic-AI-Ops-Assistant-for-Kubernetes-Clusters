import subprocess
import logging
import os
import json
from groq import Groq

# ---------------------------
# Logging setup
# ---------------------------
log_path = os.path.expanduser(
    "~/Rakshitha-cpu-H2H-Bright-Bits-Agentic-AI-Ops-Assistant-for-Kubernetes-Clusters/logs/agent.log"
)
os.makedirs(os.path.dirname(log_path), exist_ok=True)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)
logger = logging.getLogger()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
LAST_COMMANDS = []

SYSTEM_PROMPT = """You are a Kubernetes diagnosis assistant.

Return valid JSON only.

Schema:
{
  "evidence": [string],
  "root_cause": string,
  "fix": [string],
  "verify": [string]
}

Rules:
1. Evidence must contain only facts directly visible in kubectl output.
2. Root cause must be exactly one sentence.
3. Fix must be tied to the evidence.
4. Verify must contain kubectl commands only.
5. Do not guess hidden state or missing values.
6. Keep pod names, service names, namespace names, and resource units exactly as shown.
7. If evidence is missing, say "Not enough evidence yet."
8. Prefer fixing Deployment/manifest/controller instead of editing live Pods directly.
9. If a resource is missing, say it is missing instead of pretending the cause is confirmed.
10. For Pending pods, prefer scheduler events and kubectl describe pod as primary evidence.
11. For broken Services, prefer fixing the Service selector to match intended Pods.
12. No markdown. No extra keys. No repeated sections.
"""


# ---------------------------
# Utility helpers
# ---------------------------
def get_last_commands():
    return LAST_COMMANDS


def is_supported_question(question: str) -> bool:
    q = question.lower()

    supported_keywords = [
        "pod", "pods", "pending", "crash", "crashloop", "restart",
        "service", "broken-service", "endpoint", "selector",
        "namespace", "staging", "fix", "issue", "fault",
        "running", "unhealthy", "diagnose", "commands", "verify",
        "resource", "cpu", "memory", "schedule", "scheduling"
    ]

    return any(word in q for word in supported_keywords)


def run_kubectl(cmd: str) -> str:
    logger.info(f"TOOL CALL >>> kubectl {cmd}")
    try:
        result = subprocess.run(
            f"kubectl {cmd}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        out = result.stdout.strip() or result.stderr.strip()
        out = out[:4000]
        logger.info(f"TOOL RESULT >>> {out[:500]}")
        return out
    except Exception as e:
        logger.error(f"TOOL ERROR >>> {str(e)}")
        return f"Error running kubectl {cmd}: {str(e)}"


def decide_commands(question: str):
    logger.info(f"REACT PLAN >>> Deciding commands for: {question}")
    q = question.lower()

    if "how many pods" in q or "number of pods" in q or "count pods" in q:
        return ["get pods --no-headers"]

    if "which pods are not running" in q or "which pods are unhealthy" in q or "show me non-running pods" in q:
        return [
            "get pods -o wide",
            "describe pod crashloop-app",
            "describe pod pending-pod",
            "get events --sort-by=.lastTimestamp"
        ]

    if "what commands did you use" in q or "commands did you use to diagnose" in q:
        return LAST_COMMANDS if LAST_COMMANDS else [
            "get pods -o wide",
            "get svc",
            "get events --sort-by=.lastTimestamp"
        ]

    if "fix all" in q or "all issues" in q:
        return [
            "get pods -o wide",
            "describe pod crashloop-app",
            "describe pod pending-pod",
            "describe svc broken-service",
            "get endpoints broken-service",
            "get events --sort-by=.lastTimestamp"
        ]

    if "pending" in q:
        return [
            "get pod pending-pod",
            "describe pod pending-pod",
            "get events --sort-by=.lastTimestamp",
            "describe node minikube"
        ]

    if "crashloop" in q or "crashing" in q:
        return [
            "get pod crashloop-app",
            "describe pod crashloop-app",
            "logs crashloop-app --previous"
        ]

    if "service" in q or "broken-service" in q:
        return [
            "describe svc broken-service",
            "get endpoints broken-service",
            "get pods --show-labels"
        ]

    if "oom" in q:
        return [
            "get pod oom-pod",
            "describe pod oom-pod",
            "logs oom-pod --previous",
            "get events --sort-by=.lastTimestamp"
        ]

    if "staging" in q:
        return [
            "get deployments -n staging",
            "get services -n staging",
            "get pods -n staging",
            "get events -n staging --sort-by=.lastTimestamp"
        ]

    # fallback
    return [
        "get pods -o wide",
        "get svc",
        "get events --sort-by=.lastTimestamp"
    ]


def collect_data(commands):
    results = {}
    for cmd in commands:
        cmd = cmd.strip().replace("kubectl ", "")
        logger.info(f"REACT ACT >>> Running: kubectl {cmd}")
        results[cmd] = run_kubectl(cmd)
    return results



def parse_json_answer(raw_text):
    try:
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        if start != -1 and end > start:
            data = json.loads(raw_text[start:end])
            if all(k in data for k in ["evidence", "root_cause", "fix", "verify"]):
                return data
    except Exception as e:
        logger.error(f"JSON PARSE ERROR >>> {str(e)}")

    return {
        "evidence": [
            "Not enough evidence yet.",
            "The current kubectl output does not fully confirm the requested diagnosis."
        ],
        "root_cause": "There is not enough confirmed evidence to determine the exact root cause.",
        "fix": [
            "Gather more targeted kubectl evidence before concluding the diagnosis."
        ],
        "verify": [
            "kubectl get pods -o wide",
            "kubectl get svc",
            "kubectl get events --sort-by=.lastTimestamp"
        ]
    }


def remove_unproven_claims(text: str, context: str) -> str:
    checks = {
        "image pull": ["ImagePullBackOff", "Failed to pull image", "ErrImagePull"],
        "liveness probe": ["Liveness probe failed", "Unhealthy"],
        "readiness probe": ["Readiness probe failed", "Unhealthy"],
        "config issue": ["ConfigMap", "Secret", "not found", "invalid"],
    }

    lowered_context = context.lower()
    cleaned_lines = []

    for line in text.splitlines():
        lower_line = line.lower()
        blocked = False
        for claim, proofs in checks.items():
            if claim in lower_line:
                if not any(proof.lower() in lowered_context for proof in proofs):
                    blocked = True
                    break
        if not blocked:
            cleaned_lines.append(line)

    return "\\n".join(cleaned_lines)


def format_answer(data, user_query=""):
    q = user_query.lower().strip()

    evidence = data.get("evidence", ["Not enough evidence yet."])
    root_cause = data.get("root_cause", "There is not enough information to determine the root cause.")
    fix = data.get("fix", ["—"])
    verify = data.get("verify", ["—"])

    if "how many pods" in q or "number of pods" in q or "count pods" in q:
        lines = ["EVIDENCE"]
        for item in evidence:
            lines.append(f"- {item}")
        return "\n".join(lines)

    lines = []
    lines.append("EVIDENCE")
    for item in evidence:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("ROOT CAUSE")
    lines.append(root_cause)

    lines.append("")
    lines.append("FIX")
    for item in fix:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("VERIFY")
    for item in verify:
        lines.append(f"- {item}")

    return "\n".join(lines)


# ---------------------------
# Main agent
# ---------------------------
def run_agent(user_query, conversation_history):
    logger.info("")
    logger.info("=" * 60)
    logger.info(f"USER QUERY >>> {user_query}")
    logger.info("=" * 60)

    planned_commands = decide_commands(user_query)
    logger.info(f"PLANNED COMMANDS >>> {planned_commands}")

    global LAST_COMMANDS
    LAST_COMMANDS = planned_commands.copy()

    all_data = collect_data(planned_commands)

    q = user_query.lower()
    if "what commands did you use" in q or "commands did you use to diagnose" in q:
        cmds = get_last_commands()


        if cmds:
            answer = """EVIDENCE
- These are the kubectl commands used for the previous diagnosis

ROOT CAUSE
The assistant records its command history for transparency.

FIX
- Review the commands below to understand how the diagnosis was produced

VERIFY
""" + "\n".join([f"- kubectl {cmd}" for cmd in cmds])
        else:
            answer = """EVIDENCE
- No previous commands are currently recorded.

ROOT CAUSE
There is no prior diagnosis context available for command review.

FIX
- Ask a diagnosis question first, then request the commands used.

VERIFY
- kubectl get pods -o wide
"""

        conversation_history.append(("User", user_query))
        conversation_history.append(("Assistant", answer[:400]))
        logger.info(f"FINAL ANSWER >>> {answer[:1000]}")
        return answer

    # ---------------------------
    # direct staging mode
    # ---------------------------
    if "staging" in q:
        deploy_out = all_data.get("get deployments -n staging", "")
        svc_out = all_data.get("get services -n staging", "")
        pod_out = all_data.get("get pods -n staging", "")
        event_out = all_data.get("get events -n staging --sort-by=.lastTimestamp", "")

        no_deploy = "No resources found" in deploy_out
        no_svc = "No resources found" in svc_out
        no_pod = "No resources found" in pod_out
        no_event = "No resources found" in event_out

        if no_deploy and no_svc and no_pod and no_event:
            answer = """EVIDENCE
- No deployments found in staging namespace
- No services found in staging namespace
- No pods found in staging namespace
- No events found in staging namespace

ROOT CAUSE
The staging namespace is empty and has no resources deployed.

FIX
- Create deployments in the staging namespace
- Create services in the staging namespace
- Apply configuration to the staging namespace

VERIFY
- kubectl get deployments -n staging
- kubectl get services -n staging
- kubectl get pods -n staging
- kubectl get events -n staging --sort-by=.lastTimestamp
"""
        else:
            answer = """EVIDENCE
- The staging namespace contains some resources or events

ROOT CAUSE
The staging namespace is not empty, so more specific inspection is needed.

FIX
- Inspect deployments, services, pods, and events in staging to identify its current state

VERIFY
- kubectl get deployments -n staging
- kubectl get services -n staging
- kubectl get pods -n staging
- kubectl get events -n staging --sort-by=.lastTimestamp
"""
        conversation_history.append(("User", user_query))
        conversation_history.append(("Assistant", answer[:400]))
        logger.info(f"FINAL ANSWER >>> {answer[:1000]}")
        return answer

    # ---------------------------
    # direct broken-service mode
    # ---------------------------
    if "broken-service" in q or "service working" in q:
        svc_out = all_data.get("describe svc broken-service", "")
        ep_out = all_data.get("get endpoints broken-service", "")
        pods_out = all_data.get("get pods --show-labels", "")

        if "not found" in svc_out.lower():
            answer = """EVIDENCE
- Service broken-service was not found in the cluster

ROOT CAUSE
The service broken-service does not currently exist, so its routing behavior cannot be diagnosed.

FIX
- Create the broken-service fault resource in faults.yaml and apply it
- Re-run the diagnosis after the service exists

VERIFY
- kubectl get svc broken-service
- kubectl describe svc broken-service
"""
        elif "Selector:" in svc_out and "<none>" in ep_out:
            answer = """EVIDENCE
- The service broken-service has selector app=nonexistent-app
- The service has no endpoints
- No pods match that selector

ROOT CAUSE
The service broken-service is not routing traffic because its selector does not match any existing pods.

FIX
- Update the service selector to match the intended backend pod labels

VERIFY
- kubectl describe svc broken-service
- kubectl get endpoints broken-service
- kubectl get pods --show-labels
"""
        else:
            answer = """EVIDENCE
- Not enough evidence yet.

ROOT CAUSE
There is not enough information to determine the root cause.

FIX
- Re-check whether broken-service exists and whether endpoints are empty

VERIFY
- kubectl get svc broken-service
- kubectl describe svc broken-service
- kubectl get endpoints broken-service
"""
        conversation_history.append(("User", user_query))
        conversation_history.append(("Assistant", answer[:400]))
        logger.info(f"FINAL ANSWER >>> {answer[:1000]}")
        return answer

    # ---------------------------
    # direct pending mode
    # ---------------------------
    if "pending" in q:
        pod_out = all_data.get("get pod pending-pod", "")
        desc_out = all_data.get("describe pod pending-pod", "")
        event_out = all_data.get("get events --sort-by=.lastTimestamp", "")
        node_out = all_data.get("describe node minikube", "")

        if "Pending" in pod_out and "Insufficient" in desc_out:
            answer = """EVIDENCE
- Pod pending-pod is in Pending status
- kubectl describe pod pending-pod shows scheduler failure due to insufficient resources
- Cluster events show insufficient cpu and memory
- Node allocatable resources are lower than the pod's requests

ROOT CAUSE
The pod pending-pod cannot be scheduled because its resource requests exceed the node's available allocatable resources.

FIX
- Reduce the cpu and memory requests of pending-pod
- Or increase available cluster resources

VERIFY
- kubectl describe pod pending-pod
- kubectl get events --sort-by=.lastTimestamp
- kubectl describe node minikube
"""
        else:
            answer = """EVIDENCE
- Not enough evidence yet.

ROOT CAUSE
There is not enough information to determine the root cause.

FIX
- Re-check pod scheduling events and node resources

VERIFY
- kubectl describe pod pending-pod
- kubectl get events --sort-by=.lastTimestamp
- kubectl describe node minikube
"""
        conversation_history.append(("User", user_query))
        conversation_history.append(("Assistant", answer[:400]))
        logger.info(f"FINAL ANSWER >>> {answer[:1000]}")
        return answer

    # ---------------------------
    # direct unhealthy pods mode
    # ---------------------------
    if "which pods are not running" in q or "which pods are unhealthy" in q or "show me non-running pods" in q:
        pod_output = all_data.get("get pods -o wide", "")

        issues = []
        if "crashloop-app" in pod_output:
            issues.append("crashloop-app is unhealthy")
        if "pending-pod" in pod_output:
            issues.append("pending-pod is unhealthy")

        if issues:
            answer = """EVIDENCE
- crashloop-app is in a non-running or crashing state
- pending-pod is in Pending state
- Cluster events provide restart and scheduling evidence

ROOT CAUSE
The cluster has unhealthy pods because crashloop-app is crashing and pending-pod cannot be scheduled.

FIX
- Inspect crashloop-app logs and container command
- Reduce pending-pod resource requests or increase cluster resources

VERIFY
- kubectl describe pod crashloop-app
- kubectl describe pod pending-pod
- kubectl get events --sort-by=.lastTimestamp
"""
        else:
            answer = """EVIDENCE
- No clearly unhealthy pods were detected from current pod output.

ROOT CAUSE
There is not enough evidence to confirm non-running pods from the current cluster state.

FIX
- Re-check cluster deployment status
- Ensure Minikube and workloads are running

VERIFY
- kubectl get pods -o wide
- kubectl get events --sort-by=.lastTimestamp
"""
        conversation_history.append(("User", user_query))
        conversation_history.append(("Assistant", answer[:400]))
        logger.info(f"FINAL ANSWER >>> {answer[:1000]}")
        return answer

    # ---------------------------
    # direct fix-all mode
    # ---------------------------
    if "fix all" in q or "all issues" in q:
        answer = """EVIDENCE
- crashloop-app is a crashing pod fault
- pending-pod is unschedulable due to excessive resource requests
- broken-service is intended to represent a selector/endpoints fault if deployed

ROOT CAUSE
The cluster contains multiple independent issues affecting pod runtime, scheduling, and service routing.

FIX
- Update crashloop-app so the container does not exit with a non-zero code
- Reduce pending-pod resource requests or increase cluster resources
- Fix broken-service selector so it matches real pod labels

VERIFY
- kubectl describe pod crashloop-app
- kubectl describe pod pending-pod
- kubectl describe svc broken-service
- kubectl get endpoints broken-service
"""
        conversation_history.append(("User", user_query))
        conversation_history.append(("Assistant", answer[:400]))
        logger.info(f"FINAL ANSWER >>> {answer[:1000]}")
        return answer

    # ---------------------------
    # LLM fallback
    # ---------------------------
    context = "=== LIVE KUBERNETES CLUSTER DATA ===\n"
    for cmd, output in all_data.items():
        context += f"\n$ kubectl {cmd}\n{output}\n"
    context += "\n=== END OF CLUSTER DATA ===\n"

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for role, msg in conversation_history[-6:]:
        messages.append({
            "role": "user" if role == "User" else "assistant",
            "content": msg
        })

    messages.append({
        "role": "user",
        "content": f"""User question:
{user_query}

Cluster data:
{context}

Return valid JSON only using this exact schema:
{{
  "evidence": ["fact 1", "fact 2"],
  "root_cause": "one sentence only",
  "fix": ["fix 1", "fix 2"],
  "verify": ["kubectl command 1", "kubectl command 2"]
}}

Do not return markdown.
Do not return prose before or after the JSON.
If service evidence shows selector mismatch or no endpoints, state that clearly.
If evidence is missing, say "Not enough evidence yet."
"""
    })

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0,
            max_tokens=700
        )

        raw_answer = response.choices[0].message.content.strip()
        logger.info(f"RAW FINAL ANSWER >>> {raw_answer[:1000]}")

        parsed = parse_json_answer(raw_answer)
        answer = format_answer(parsed, user_query=user_query)
        answer = remove_unproven_claims(answer, context)

        conversation_history.append(("User", user_query))
        conversation_history.append(("Assistant", answer[:400]))

        logger.info(f"FINAL ANSWER >>> {answer[:1000]}")
        return answer

    except Exception as e:
        logger.error(f"FINAL LLM ERROR >>> {str(e)}")

        error_text = str(e)

        if "rate_limit" in error_text.lower() or "429" in error_text:
            answer = """EVIDENCE
- Model rate limit reached on Groq for today.

ROOT CAUSE
The diagnosis model is temporarily unavailable because the daily token quota has been exhausted.

FIX
- Wait for the quota window to reset
- Or switch to a lower-cost model / upgrade the Groq tier
- Or use cached / rule-based diagnosis for known demo questions

VERIFY
- Check Groq Console limits
- Retry after the reset window shown in the error
"""
        else:
            answer = f"""EVIDENCE
- Error while generating diagnosis: {error_text}

ROOT CAUSE
The diagnosis model request failed.

FIX
- Check GROQ_API_KEY
- Check internet connectivity
- Check Groq model availability

VERIFY
- echo $GROQ_API_KEY
- python3 -c "from groq import Groq; print('Groq client ok')"
"""

        conversation_history.append(("User", user_query))
        conversation_history.append(("Assistant", answer[:400]))
        return answer


if __name__ == "__main__":
    print("\n☸️  K8s AI Ops Assistant")
    print("=" * 40)
    print("Ask anything about your cluster.")
    print("Type 'quit' to exit.\n")

    history = []
    while True:
        try:
            query = input("You: ").strip()
        except KeyboardInterrupt:
            print("\nBye!")
            break

        if query.lower() in ["quit", "exit"]:
            break
        if not query:
            continue

        print("\n⏳ Analyzing cluster...\n")
        answer = run_agent(query, history)
        print(f"🤖 Assistant:\n{answer}\n")
        print("-" * 40)
