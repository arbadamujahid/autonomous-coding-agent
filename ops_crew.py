import ollama
import subprocess
import asyncio

from mcp import Client, StdioServerParameters


MODEL = "qwen2.5-coder:1.5b"


def run_agent(role, task):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": role
            },
            {
                "role": "user",
                "content": task
            }
        ]
    )

    return response["message"]["content"]


async def main():

    # ==============================
    # USER TASK
    # ==============================

    task = input("What do you want the Ops Crew to build? ")

    # ==============================
    # REAL MCP CONNECTION
    # ==============================

    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )

    async with Client(server_params) as client:

        tools_result = await client.list_tools()

        print("\n🔌 REAL MCP CONNECTION")
        print("Available MCP tools:")

        for tool in tools_result.tools:
            print("•", tool.name)

        # ==============================
        # PLANNER
        # ==============================

        print("\n🧠 Planner is working...")

        plan = run_agent(
            "You are the planning agent. "
            "Create a simple step-by-step plan. "
            "Do not write code.",
            task
        )

        print("\n📋 PLAN:")
        print(plan)

        # ==============================
        # CODER
        # ==============================

        print("\n💻 Coder is working...")

        code = run_agent(
    "You are the coding agent. "
    "Write valid Python code based on the task and plan. "
    "If the task requires user values, use input() to ask the user for those values. "
    "Do not hardcode example values unless the task explicitly asks for them. "
    "Return only Python code.",
            
            f"""
Task:
{task}

Plan:
{plan}
"""
        )

        # Remove markdown formatting if the model adds it
        code = code.replace("```python", "")
        code = code.replace("```", "")
        code = code.strip()

        print("\n✅ CODE GENERATED:")
        print(code)

        # ==============================
        # REVIEWER
        # ==============================

        print("\n🔍 Reviewer is working...")

        review = run_agent(
            "You are a code reviewer. "
            "Check the Python code for errors or possible bugs. "
            "Give a short review.",
            f"""
Task:
{task}

Generated code:
{code}
"""
        )

        print("\n📝 REVIEW:")
        print(review)

        # ==============================
        # SAVE USING REAL MCP
        # ==============================

        print("\n💾 Saving code using REAL MCP...")

        save_result = await client.call_tool(
            "write_project_file",
            {
                "file_path": "projects/generated_code.py",
                "content": code
            }
        )

        print("✅ Code saved using REAL MCP!")

        # ==============================
        # READ USING REAL MCP
        # ==============================

        print("\n📖 Reading generated code using REAL MCP...")

        read_result = await client.call_tool(
            "read_project_file",
            {
                "file_path": "projects/generated_code.py"
            }
        )

        print("✅ Code successfully read through MCP!")

        # ==============================
        # EXECUTOR
        # ==============================

        print("\n▶️ Executor is running...")

        result = subprocess.run(
            ["python", "projects/generated_code.py"],
            text=True
        )

        # ==============================
        # DEBUGGER
        # ==============================

        if result.returncode != 0:

            print("\n❌ Execution failed!")

            print("\n🐛 Debugger is working...")

            fixed_code = run_agent(
                "You are the debugging agent. "
                "Fix the Python code so that it runs correctly. "
                "Return ONLY corrected Python code. "
                "Do not include markdown or explanations.",
                f"""
Task:
{task}

Code:
{code}

The program failed during execution.

Fix the code and return only valid Python code.
"""
            )

            fixed_code = fixed_code.replace("```python", "")
            fixed_code = fixed_code.replace("```", "")
            fixed_code = fixed_code.strip()

            # Save corrected code through MCP
            await client.call_tool(
                "write_project_file",
                {
                    "file_path": "projects/generated_code.py",
                    "content": fixed_code
                }
            )

            print("\n🔧 Code fixed using MCP!")

            print("\n▶️ Running corrected program...")

            fixed_result = subprocess.run(
                ["python", "projects/generated_code.py"],
                text=True
            )

            if fixed_result.returncode == 0:
                print("\n✅ Corrected program completed successfully!")
            else:
                print("\n❌ Corrected program still has an error.")

        else:

            print("\n✅ Program completed successfully!")

        # ==============================
        # MCP PROJECT SUMMARY
        # ==============================

        print("\n" + "=" * 50)
        print("🚀 OPS CREW COMPLETED")
        print("=" * 50)

        print("🧠 Planner      ✓")
        print("💻 Coder        ✓")
        print("🔍 Reviewer     ✓")
        print("▶️ Executor     ✓")
        print("🐛 Debugger     ✓")
        print("🔌 Real MCP     ✓")
        print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())