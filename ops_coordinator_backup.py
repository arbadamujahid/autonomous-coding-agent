import ollama

MODEL = "qwen2.5-coder:1.5b"


def coordinator(task):

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You are the Ops Coordinator of an autonomous coding agent.

Your job is to analyze the user's coding task and decide which agents are needed.

Available agents:
1. Planner
2. Coder
3. Reviewer
4. Executor
5. Debugger

Return a simple execution plan showing the order in which these agents should work.
Do not write code.
"""
            },
            {
                "role": "user",
                "content": task
            }
        ]
    )

    return response["message"]["content"]


def main():

    task = input("What do you want the Ops Crew to build? ")

    print("\n🎯 Ops Coordinator is analyzing the task...")

    plan = coordinator(task)

    print("\n🗺️ OPS CREW PLAN:")
    print(plan)


if __name__ == "__main__":
    main()