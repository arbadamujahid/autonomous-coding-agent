import subprocess
import sys

def main():

    task = input("What do you want the Ops Crew to build? ")

    print("\n🎯 OPS COORDINATOR")
    print("Task received:", task)

    print("\n🗺️ OPS CREW WORKFLOW")
    print("1. 🧠 Planner")
    print("2. 💻 Coder")
    print("3. 🔍 Reviewer")
    print("4. ▶️ Executor")
    print("5. 🐛 Debugger")

    print("\n🚀 Starting Ops Crew...\n")

    subprocess.run(
        [sys.executable, "ops_crew.py"]
    )


if __name__ == "__main__":
    main()