from pathlib import Path

current_dir = Path.cwd()
current_file = Path(__file__).name

print(f"files in {current_dir}:")
for file in current_dir.iterdir():
    if file.name == current_file:
        continue

    print(f"  - {file.name}")

    if file.is_file():
        content = file.read_text(encoding="utf-8")
        print(f"    content: {content}")
    