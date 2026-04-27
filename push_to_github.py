"""
Codex 005 · Push prompt to GitHub
─────────────────────────────────
Sube `prompts/reels_estrategia.txt` al repo `jorgeluis666/codex005`.

Uso:
    1. Configura tu Personal Access Token con permisos `repo`:
         PowerShell:  $env:GITHUB_TOKEN = "ghp_xxx..."
         CMD:         set GITHUB_TOKEN=ghp_xxx...
         Bash:        export GITHUB_TOKEN="ghp_xxx..."
    2. Instala PyGithub si no lo tienes:
         pip install PyGithub
    3. Ejecuta:
         python push_to_github.py
"""

import os
from pathlib import Path

from github import Github, GithubException

REPO        = "jorgeluis666/codex005"
LOCAL_FILE  = Path(__file__).parent / "prompts" / "reels_estrategia.txt"
REMOTE_PATH = "prompts/reels_estrategia.txt"
COMMIT_MSG  = "Añadir prompt para estrategia de reels"
BRANCH      = "main"


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit(
            "Falta GITHUB_TOKEN en el entorno. "
            "Configúralo con tu Personal Access Token antes de ejecutar."
        )

    if not LOCAL_FILE.exists():
        raise SystemExit(f"No encontré el archivo local: {LOCAL_FILE}")

    contenido = LOCAL_FILE.read_text(encoding="utf-8")

    repo = Github(token).get_repo(REPO)

    try:
        existing = repo.get_contents(REMOTE_PATH, ref=BRANCH)
    except GithubException as exc:
        if exc.status != 404:
            raise
        repo.create_file(
            path=REMOTE_PATH,
            message=COMMIT_MSG,
            content=contenido,
            branch=BRANCH,
        )
        print(f"✓ Creado {REPO}:{REMOTE_PATH}")
        return

    if existing.decoded_content.decode("utf-8") == contenido:
        print("✓ Sin cambios — el archivo remoto ya está al día.")
        return

    repo.update_file(
        path=REMOTE_PATH,
        message=f"{COMMIT_MSG} (actualizar)",
        content=contenido,
        sha=existing.sha,
        branch=BRANCH,
    )
    print(f"✓ Actualizado {REPO}:{REMOTE_PATH}")


if __name__ == "__main__":
    main()
