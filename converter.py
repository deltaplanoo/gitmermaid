import os
from git import Repo, GitCommandError
import tempfile

def generate_limited_mermaid_gitgraph(repo_url, limit=8):
    temp_dir = tempfile.mkdtemp()
    print(f"--- Clonazione di {repo_url} in corso... ---")
    
    try:
        # Clonazione shallow (depth) non sempre ideale per i branch, 
        # quindi cloniamo normalmente ma filtriamo i commit dopo.
        repo = Repo.clone_from(repo_url, temp_dir, bare=True)
    except GitCommandError as e:
        return f"Errore durante la clonazione: {e}"

    # Recuperiamo gli ultimi N commit (ordinati dal più recente al più vecchio)
    all_commits = list(repo.iter_commits('--all', max_count=limit))
    
    # Invertiamo la lista per Mermaid (che vuole l'ordine cronologico: vecchio -> nuovo)
    commits = all_commits[::-1]
    
    mermaid_code = ["gitGraph"]
    created_branches = set(["main", "master"])
    current_branch = "main"

    for commit in commits:
        # Trova a quale branch appartiene il commit
        try:
            branches = repo.git.branch("--contains", commit.hexsha).replace("*", "").split()
        except:
            branches = ["main"] # Fallback se non trovato

        if branches:
            target_branch = branches[0]
            # Gestione creazione branch in Mermaid
            if target_branch not in created_branches:
                mermaid_code.append(f"    branch {target_branch}")
                created_branches.add(target_branch)
            
            # Switch del branch se necessario
            if target_branch != current_branch:
                mermaid_code.append(f"    checkout {target_branch}")
                current_branch = target_branch

        # Identificazione Merge vs Commit semplice
        if len(commit.parents) > 1:
            # Semplificazione: merge dal "main" se non riusciamo a determinare il parent secondario
            mermaid_code.append(f"    merge {target_branch} id: \"{commit.hexsha[:7]}\"")
        else:
            mermaid_code.append(f"    commit id: \"{commit.hexsha[:7]}\"")

    return "\n".join(mermaid_code)

if __name__ == "__main__":
    # input_repo_link = input("Inserisci l'URL della repository GitHub: ")
    repo_link = "https://github.com/deltaplanoo/Agentic-Probability-Engine"
    risultato = generate_limited_mermaid_gitgraph(repo_link, limit=8)
    
    print("\n--- CODICE MERMAID (ULTIMI 8 COMMIT) ---\n")
    print(risultato)
    print("\n----------------------------------------\n")
    print("Incolla il codice su https://mermaid.live per visualizzarlo.")