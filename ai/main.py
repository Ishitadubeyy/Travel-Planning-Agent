import os
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
print("API KEY:", API_KEY)


# -----------------------------
# LLM Call
# -----------------------------
def call_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI-Agent-Project"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    print("\nDEBUG RESPONSE:\n", response.text)

    res_json = response.json()

    if "choices" not in res_json:
        return f"ERROR: {res_json}"

    return res_json["choices"][0]["message"]["content"]


# -----------------------------
# Tools
# -----------------------------
def search_tool(query):
    print(f"\n[TOOL: SEARCH] {query}")

    if "hotel" in query.lower():
        return "Hotels in Goa cost approx INR 1500 per night"
    elif "places" in query.lower():
        return "Baga Beach, Anjuna Beach, Fort Aguada"
    elif "travel" in query.lower():
        return "Travel cost approx INR 2000"
    
    return "General travel info available"


def calculator_tool(expression):
    print(f"\n[TOOL: CALCULATOR] {expression}")

    try:
        return str(eval(expression))
    except:
        return "Error in calculation"


# -----------------------------
# Agent Loop
# -----------------------------
def agent(user_goal):
    print(f"\nUSER GOAL: {user_goal}\n")
    context = ""

    for step in range(5):
        prompt = f"""
You are an AI Travel Planning Agent.
Follow this format strictly:

Thought: What to do next
Action: Search or Calculator or Final
Action Input: Input for the action

Previous context:
{context}

User goal:
{user_goal}
"""

        output = call_llm(prompt)
        print(f"\nLLM OUTPUT:\n{output}\n")

        if "Final" in output:
            return output

        if "Search" in output:
            query = output.split("Action Input:")[-1].strip()
            obs = search_tool(query)

        elif "Calculator" in output:
            expr = output.split("Action Input:")[-1].strip()
            obs = calculator_tool(expr)

        else:
            return "Error: Unknown Action"

        context += f"\n{output}\nObservation: {obs}\n"

    return "Max steps reached"


# -----------------------------
# USER INPUT
# -----------------------------
user_goal = input("Enter your travel goal: ")

result = agent(user_goal)

print("\n====== FINAL RESULT ======\n")
print(result)