import os
import tempfile
from git import Repo


# === VARS === #
last_n_commits = 20
repo_url = ""


def generate_mermaid(repo_url, limit=last_n_commits):
    temp_dir = tempfile.mkdtemp()
    repo = Repo.clone_from(repo_url, temp_dir, bare=True)
    
    log_data = repo.git.log(f'--all', f'--max-count={limit}', '--reverse', '--format=%H %D').split('\n')
    
    mermaid = ["gitGraph"]
    created_branches = set(["main", "master"])
    current_branch = "main"
    
    for line in log_data:
        if not line.strip(): continue
        parts = line.split(' ', 1)
        sha = parts[0]
        short_sha = sha[:7]
        refs = parts[1] if len(parts) > 1 else ""

        target_branch = None
        if "web_search" in refs:
            target_branch = "web_search"
        elif "LangGraph" in refs:
            target_branch = "LangGraph"
        elif "main" in refs or "master" in refs:
            target_branch = "main"
        
        if not target_branch:
            target_branch = current_branch

        # change branch
        if target_branch != current_branch:
            if target_branch not in created_branches:
                mermaid.append(f"    branch {target_branch}")
                created_branches.add(target_branch)
            
            mermaid.append(f"    checkout {target_branch}")
            current_branch = target_branch

        mermaid.append(f"    commit id: \"{short_sha}\"")

    return "\n".join(mermaid)

if __name__ == "__main__":
    url = repo_url if repo_url else input("Enter the GitHub repository URL: ")
    print("\n" + generate_mermaid(url))