import os
import re

def normalize(text):
    """
    Normalizes a string to match problem names.
    1. Removes file extensions (e.g., .java, .py)
    2. Removes leading numbers and separators (e.g., "1_", "02-")
    3. Removes all remaining non-alphanumeric characters and lowercases.
    """
    text = os.path.splitext(text)[0]
    text = re.sub(r'^\d+[_\-\s]*', '', text)
    return re.sub(r'[^a-z0-9]', '', text.lower())

def get_all_solution_files():
    """Scans the repository for ACTUAL code solution files and returns a set of normalized names."""
    solution_files = set()
    valid_extensions = {'.py', '.java', '.cpp', '.js', '.ts', '.c', '.cs', '.go', '.rs'}
    
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '.github']
        for file in files:
            if file.startswith('.'):
                continue
            _, ext = os.path.splitext(file)
            if ext.lower() in valid_extensions:
                normalized_name = normalize(file)
                if normalized_name:
                    solution_files.add(normalized_name)
    return solution_files

def update_readme(readme_path="README.md"):
    existing_files = get_all_solution_files()
    print(f"🔍 Found {len(existing_files)} actual code solution files in repository.")
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    lines = content.split('\n')

    # 1. Update checkboxes based on code file existence
    for i, line in enumerate(lines):
        match = re.match(r'^- \[([ xX])\] (.*?)$', line)
        if match:
            problem_name = match.group(2).strip()
            normalized_problem = normalize(problem_name)
            
            if normalized_problem in existing_files:
                if line.startswith('- [ ]'):
                    lines[i] = f'- [x] {problem_name}'
                    print(f"✅ Checked: {problem_name}")
            else:
                if line.startswith('- [x]'):
                    lines[i] = f'- [ ] {problem_name}'
                    print(f"⬜ Unchecked: {problem_name} (no code file found)")

    content = '\n'.join(lines)

    # 2. Rebuild the Summary Table dynamically
    table_start = -1
    table_end = -1
    
    for i, line in enumerate(lines):
        # FIX 1: Use regex to find the header row, ignoring extra spaces
        if re.match(r'^\|\s*Chapter\s*\|', line):
            table_start = i
        if table_start != -1 and line.startswith("|") and "TOTAL" in line:
            table_end = i
            break

    if table_start != -1 and table_end != -1:
        details_blocks = re.finditer(r'<summary><b>.*?Chapter \d+: (.*?)</b></summary>(.*?)</details>', content, re.DOTALL)
        chapter_counts = {}
        for block in details_blocks:
            chapter_name = block.group(1).strip()
            block_content = block.group(2)
            solved = len(re.findall(r'- \[x\]', block_content, re.IGNORECASE))
            total = len(re.findall(r'- \[[ xX]\]', block_content))
            chapter_counts[chapter_name] = (solved, total)

        # FIX 2: Keep the header (table_start) AND the separator row (table_start + 1)
        new_lines = lines[:table_start + 2] 
        
        total_solved = 0
        total_total = 0

        # Process only the actual data rows (skipping the separator)
        for i in range(table_start + 2, table_end):
            line = lines[i]
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6 and parts[2]: 
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
        
        # Add TOTAL row
        total_percentage = int((total_solved / total_total) * 100) if total_total > 0 else 0
        total_filled = int(total_percentage / 10)
        total_bar = '█' * total_filled + '░' * (10 - total_filled)
        new_lines.append(f"| | **TOTAL** | **{total_solved}** | **{total_total}** | **{total_bar} {total_percentage}%** |")
        
        new_lines.extend(lines[table_end+1:])
        content = '\n'.join(new_lines)

    if content != original_content:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("📝 README.md updated successfully.")
        return True
    else:
        print("ℹ️ README.md is already perfectly in sync.")
        return False

if __name__ == "__main__":
    update_readme()