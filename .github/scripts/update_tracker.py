# .github/scripts/update_tracker.py
import os
import re
import sys

def normalize(text):
    """Removes leading numbers, spaces, underscores, hyphens, and lowercases the text."""
    # 1. Strip leading numbers and their following underscores/hyphens (e.g., "1_two_sum" -> "two_sum")
    text = re.sub(r'^\d+[_\-\s]*', '', text)
    # 2. Remove all other non-alphanumeric characters and lowercase
    return re.sub(r'[^a-z0-9]', '', text.lower())

def update_readme(changed_files_str, readme_path="README.md"):
    if not changed_files_str.strip():
        print("No changed files detected.")
        return False

    # 1. Parse and normalize changed file names
    changed_files = changed_files_str.split()
    normalized_files = set()
    for f in changed_files:
        basename = os.path.basename(f)
        name_without_ext = os.path.splitext(basename)[0]
        normalized_files.add(normalize(name_without_ext))
    
    print(f"Normalized files in commit: {normalized_files}")

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    lines = content.split('\n')

    # 2. Tick the checkboxes based on file names
    for i, line in enumerate(lines):
        if line.startswith('- [ ] '):
            match = re.match(r'^- \[ \] (.*?)$', line)
            if match:
                problem_name = match.group(1).strip()
                if normalize(problem_name) in normalized_files:
                    lines[i] = f'- [x] {problem_name}'
                    print(f"✅ Ticked: {problem_name}")

    content = '\n'.join(lines)

    # 3. Rebuild the Summary Table dynamically
    table_start = -1
    table_end = -1
    in_table = False

    for i, line in enumerate(lines):
        if "| Chapter | Topic | Solved | Total | Progress |" in line:
            in_table = True
            table_start = i
            continue
        if in_table and line.startswith("|") and "TOTAL" in line:
            table_end = i
            break
        if in_table and not line.startswith("|"):
            in_table = False

    if table_start != -1 and table_end != -1:
        details_blocks = re.finditer(r'<summary><b>.*?Chapter \d+: (.*?)</b></summary>(.*?)</details>', content, re.DOTALL)
        chapter_counts = {}
        for block in details_blocks:
            chapter_name = block.group(1).strip()
            block_content = block.group(2)
            solved = len(re.findall(r'- \[x\]', block_content))
            total = len(re.findall(r'- \[ \]|- \[x\]', block_content))
            chapter_counts[chapter_name] = (solved, total)

        new_lines = lines[:table_start+1] 
        total_solved = 0
        total_total = 0

        for i in range(table_start + 1, table_end):
            line = lines[i]
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6:
                topic = parts[2]
                solved, total = chapter_counts.get(topic, (0, 0))
                total_solved += solved
                total_total += total
                
                percentage = int((solved / total) * 100) if total > 0 else 0
                filled = int(percentage / 10)
                bar = '█' * filled + '░' * (10 - filled)
                
                new_line = f"| {parts[1]} | {topic} | {solved} | {total} | {bar} {percentage}% |"
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        
        total_percentage = int((total_solved / total_total) * 100) if total_total > 0 else 0
        total_filled = int(total_percentage / 10)
        total_bar = '█' * total_filled + '░' * (10 - total_filled)
        new_lines.append(f"| | **TOTAL** | **{total_solved}** | **{total_total}** | **{total_bar} {total_percentage}%** |")
        
        new_lines.extend(lines[table_end+1:])
        content = '\n'.join(new_lines)

    # 4. Save if changes were made
    if content != original_content:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("README.md updated successfully.")
        return True
    else:
        print("No matching problems found in README. No changes made.")
        return False

if __name__ == "__main__":
    # Read the changed files from the environment variable
    changed_files_env = os.environ.get("CHANGED_FILES", "")
    update_readme(changed_files_env)