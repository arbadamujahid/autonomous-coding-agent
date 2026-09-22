from mcp.server.mcpserver import MCPServer
import os

mcp = MCPServer("Autonomous Coding Agent")


@mcp.tool()
def list_project_files(folder: str = ".") -> list[str]:
    """List files in a project folder."""
    return os.listdir(folder)


@mcp.tool()
def read_project_file(file_path: str) -> str:
    """Read a text file from the project."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


@mcp.tool()
def write_project_file(file_path: str, content: str) -> str:
    """Write content to a project file."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return f"File written successfully: {file_path}"

if __name__ == "__main__":
    mcp.run()
    