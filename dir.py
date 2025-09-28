import os

def print_dir_structure(path, max_depth=2, ignore_dirs=None, level=0):
    if ignore_dirs is None:
        ignore_dirs = {'node_modules', 'venv', '.venv', '.git', '__pycache__'}

    if level > max_depth:
        return

    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return

    for entry in entries:
        full_path = os.path.join(path, entry)

        # Skip ignored directories
        if os.path.isdir(full_path) and entry in ignore_dirs:
            continue

        print("    " * level + f"📁 {entry}" if os.path.isdir(full_path) else "    " * level + f"📄 {entry}")

        # Recursively go deeper if it's a directory
        if os.path.isdir(full_path):
            print_dir_structure(full_path, max_depth, ignore_dirs, level + 1)


if __name__ == "__main__":
    base_path = "."  # Change to your desired starting path
    print_dir_structure(base_path, max_depth=2)
