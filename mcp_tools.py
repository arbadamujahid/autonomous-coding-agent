import os


def list_files(folder="."):
    return os.listdir(folder)


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def write_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


if __name__ == "__main__":
    print("📁 MCP File Tool is ready!")
    print("Files in project:")
    print(list_files("."))