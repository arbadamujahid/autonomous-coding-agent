import ollama

task = input("What do you want me to code? ")
# Ask the AI to create a plan first
plan_response = ollama.chat(
    model="qwen2.5-coder:1.5b",
    messages=[
        {
            "role": "system",
            "content": "You are a coding planner. Create a simple step-by-step plan for the coding task. Do not write code."
        },
        {
            "role": "user",
            "content": task
        }
    ]
)

plan = plan_response["message"]["content"]

print("\n🧠 Plan:")
print(plan)
response = ollama.chat(
    model="qwen2.5-coder:1.5b",
    messages=[
        {
            "role": "system",
            "content": "You are a coding agent. Return ONLY valid Python code. Do not use markdown or explanations."
        },
        {
            "role": "user",
            "content": f"""
Task:
{task}

Plan:
{plan}

Now write the Python code according to the plan.
Return only valid Python code.
"""
        }
    ]
)

code = response["message"]["content"]

# Remove Markdown code fences if the AI adds them
code = code.replace("```python", "")
code = code.replace("```", "")
code = code.strip()

import os

os.makedirs("projects", exist_ok=True)

with open("projects/generated_code.py", "w", encoding="utf-8") as file:
    file.write(code)

print("\nCode generated successfully!")
print("Saved as: projects/generated_code.py")

import subprocess

print("\nRunning the generated code...\n")

result = subprocess.run(
    ["python", "project/generated_code.py"],
    capture_output=True,
    text=True
)

# Try running and fixing the code up to 3 times
for attempt in range(3):

    print(f"\n🔄 Attempt {attempt + 1} of 3")

    result = subprocess.run(
        ["python", "project/generated_code.py"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("\nOutput:")
        print(result.stdout)
        print("Program completed successfully! ✅")


    review = ollama.chat(
        model="qwen2.5-coder:7b",
        messages=[
            {
                "role": "system",
                "content": "You are a Python code reviewer. Give a short review of the code."
            },
            {
                "role": "user",
                "content": f"""
Review this Python code for the following task:

Task:
{task}

Code:
{code}

Output:
{result.stdout}

Tell me:
1. Whether the code solves the task.
2. Any obvious problems.
3. One simple improvement if needed.
"""
            }
        ]
    )

    if result.returncode == 0:
       print("\n🔍 Code Review:")
       print(review["message"]["content"])
       break

    print("\nError detected! ❌")
    print(result.stderr)

        # Ask AI to fix the error
    fix_response = ollama.chat(
        model="qwen2.5-coder:1.5b",
        messages=[
                {
                    "role": "system",
                    "content": "You are a debugging coding agent. Return ONLY corrected Python code. Do not use markdown or explanations."
                },
                {
                    "role": "user",
                    "content": f"""
Fix this Python code.

Code:
{code}

Error:
{result.stderr}

Return only the corrected Python code.
"""
                }
            ]
        ) 
code = fix_response["message"]["content"]

        # Remove Markdown code fences
        # code = code.replace("```python", "")
code = code.replace("```", "")
code = code.strip()

        # Save the corrected code
with open("generated_code.py", "w", encoding="utf-8") as file:
            file.write(code)

print("🔧 Code automatically fixed. Trying again...")


print("\n❌ The program could not be fixed after 3 attempts.")