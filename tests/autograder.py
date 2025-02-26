import os
import git
import re
import chardet

def find_repo_dir():
    """Find the directory where the .git folder is located (i.e., the student's repo root)."""
    current_dir = os.getcwd()  # Get current working directory
    while current_dir != "/" and not os.path.isdir(os.path.join(current_dir, ".git")):
        current_dir = os.path.dirname(current_dir)  # Move up one level
    return current_dir if os.path.isdir(os.path.join(current_dir, ".git")) else None

# Locate the repository directory dynamically
REPO_DIR = find_repo_dir()
if not REPO_DIR:
    raise Exception("❌ Error: No Git repository found in the current directory or its parents.")

def get_repo():
    """Returns the Git repository object."""
    return git.Repo(REPO_DIR)

def is_branch_merged(repo, branch):
    """Check if a branch has been merged into main."""
    return branch in repo.git.branch("--merged")

def get_commit_count(repo, branch):
    """Return the number of commits in a branch."""
    return len(list(repo.iter_commits(branch)))

def check_file_exists(filename):
    """Check if a file exists in the repository."""
    return os.path.isfile(os.path.join(REPO_DIR, filename))

def check_gitignore():
    """Verify .gitignore contains required entries using regex, handling encoding issues."""
    gitignore_path = os.path.join(REPO_DIR, ".gitignore")

    try:
        # Detect file encoding
        with open(gitignore_path, "rb") as f:
            raw_data = f.read()  # Read as bytes
            detected = chardet.detect(raw_data)
            encoding = detected["encoding"] if detected["encoding"] else "utf-8"

        # Open file with detected encoding
        with open(gitignore_path, "r", encoding=encoding) as f:
            content = f.read()

        # Normalize line endings
        content = content.replace("\r\n", "\n").replace("\r", "\n")

        # Use regex to check for exact matches
        secrets_match = re.search(r"^secrets\.env\s*$", content, re.MULTILINE)
        temp_files_match = re.search(r"^temp_files/\s*$", content, re.MULTILINE)

        return bool(secrets_match and temp_files_match)

    except FileNotFoundError:
        return False


if __name__ == "__main__":
    repo = get_repo()
    print(is_branch_merged(repo,"feature-a"))
    print(is_branch_merged(repo,"feature-b"))
    print(is_branch_merged(repo,"feature-c"))
    print(get_commit_count(repo,"feature-c"))
    print(check_file_exists("config.txt"))
    print(check_gitignore())

    
        
