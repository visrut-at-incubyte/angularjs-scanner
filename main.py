PROJECT_DIR = "C:\\Users\\DELL\\Desktop\\stackstore"
IGNORE_DIR_PATTERNS = str("**/node_modules/**,**/dist/**,**/*.min.js,**/.sonarqube/**,.git/**").split(",")

# imports
import os
import re
import fnmatch
import pandas as pd
from collections import defaultdict

# types
from typing import List, Dict

def find_files(base_dir: str, file_pattern: str, ignore_patterns: List[str]) -> List[str]:
    matches = []

    def is_ignored_path(path: str) -> bool:
        """Check if the path matches any of the ignore patterns."""
        return any(fnmatch.fnmatch(path, pattern) for pattern in ignore_patterns)

    for root, dirs, files in os.walk(base_dir, topdown=True):
        # Filter directories and paths to ignore
        dirs[:] = [d for d in dirs if not is_ignored_path(os.path.join(root, d))]
        for filename in files:
            file_path = os.path.join(root, filename)
            if fnmatch.fnmatch(filename, file_pattern) and not is_ignored_path(file_path):
                matches.append(file_path)
    return matches

def categorize_js_files(file_paths: List[str]) -> List[Dict[str, str]]:
    categorized_files = []
    
    patterns = {
        'module': re.compile(r'angular\s*\.\s*module\([\'"]([^\'"]+)[\'"],\s*\[[^\]]*?\]\)', re.DOTALL),
        'controller': re.compile(r'\.controller\([\'"]([^\'"]+)[\'"],(\s*\[[^,]*,)?\s*function', re.DOTALL),
        'service': re.compile(r'\.service\([\'"]([^\'"]+)[\'"],(\s*\[[^,]*,)?\s*function', re.DOTALL),
        'directive': re.compile(r'\.directive\([\'"]([^\'"]+)[\'"],(\s*\[[^,]*,)?\s*function', re.DOTALL),
        'factory': re.compile(r'\.factory\([\'"]([^\'"]+)[\'"],(\s*\[[^,]*,)?\s*function', re.DOTALL),
        'value': re.compile(r'\.value\([\'"]([^\'"]+)[\'"],\s*\[[^\]]*?\]\)', re.DOTALL)
    }

    for path in file_paths:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            loc = len(content.split('\n'))
            for type_name, pattern in patterns.items():
                if pattern.search(content):
                    categorized_files.append({'path': os.path.relpath(path, PROJECT_DIR), 'type': type_name, 'loc': loc, 'content': content})
    
    return categorized_files

def categorize_cofee_script_files(file_paths: List[str]) -> List[Dict[str, str]]:
    categorized_files = []
    
    patterns = {
        'module': re.compile(r'angular\.module\s*\[?[\'"]([^\'"]+)[\'"]\s*,\s*\[[^\]]*\]', re.DOTALL),
        'controller': re.compile(r'\.controller\s*\([\'"]([^\'"]+)[\'"]\s*,(\s*[^>]*)?\s*.', re.DOTALL),
        'service': re.compile(r'\.service\s*\([\'"]([^\'"]+)[\'"]\s*,(\s*[^>]*)?\s*.', re.DOTALL),
        'directive': re.compile(r'\.directive\s*\([\'"]([^\'"]+)[\'"]\s*,(\s*[^>]*)?\s*.', re.DOTALL),
        'factory': re.compile(r'\.factory\s*\([\'"]([^\'"]+)[\'"]\s*,(\s*[^>]*)?\s*.', re.DOTALL),
        'value': re.compile(r'\.value\s*\([\'"]([^\'"]+)[\'"]\s*,(\s*[^>]*)?\s*.', re.DOTALL),
        'constant': re.compile(r'\.constant\s*\([\'"]([^\'"]+)[\'"]\s*,(\s*[^>]*)?\s*.', re.DOTALL),
    }

    for path in file_paths:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            loc = len(content.split('\n'))
            for type_name, pattern in patterns.items():
                if pattern.search(content):
                    categorized_files.append({'path': os.path.relpath(path, PROJECT_DIR), 'type': type_name, 'loc': loc, 'content': content})
    
    return categorized_files

def categorize_html_files(file_paths: List[str]) -> List[Dict[str, str]]:
    categorized_files = []
    for path in file_paths:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            loc = len(content.split('\n'))
            categorized_files.append({'path': os.path.relpath(path, PROJECT_DIR), 'type': 'html', 'loc': loc, 'content': content})
    return categorized_files

js_files = categorize_js_files(find_files(PROJECT_DIR, "*.js", IGNORE_DIR_PATTERNS))
cofee_script_files = categorize_cofee_script_files(find_files(PROJECT_DIR, "*.coffee", IGNORE_DIR_PATTERNS))
html_files = categorize_html_files(find_files(PROJECT_DIR, "*.html", IGNORE_DIR_PATTERNS))

def get_overview(files: List[Dict[str, str]]) -> Dict[str, int]:
    # count total number of services, controllers, directives, etc.
    overview = defaultdict(int)
    for file in files:
        overview[file['type']] += 1
    return overview

if __name__ == "__main__":
    overview = pd.DataFrame(get_overview(js_files + html_files + cofee_script_files).items(), columns=['Type', 'Count'])
    print("Overview of the AngularJS project:")
    print(overview.to_string(index=False))
    print("----------------------------------")
    codebase = pd.DataFrame(js_files + html_files + cofee_script_files)
    codebase = codebase.drop(columns=['content'])
    codebase.to_csv("codebase.csv", index=False)