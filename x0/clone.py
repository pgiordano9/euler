import os

def clone_git_repo(url: str) -> None:
    os.system(f"git clone {url}")

clone_git_repo("https://github.com/wp-iaas/nettooling-backup-ultradns.git")
