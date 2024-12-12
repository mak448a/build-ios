from InquirerPy import inquirer
from dotenv import load_dotenv
import subprocess
import shutil
import os


load_dotenv()
USERNAME = os.getenv("USERNAME")
REPO_NAME = os.getenv("REPO_NAME")


if not USERNAME or not REPO_NAME:
    USERNAME = inquirer.text("What's your GitHub username?").execute()
    REPO_NAME = inquirer.text(
        "What's the name of the repo that you want to store your project in?"
    ).execute()


def _check_repo_exists(owner: str, repo_name: str) -> bool:
    try:
        result = subprocess.run(
            ["gh", "repo", "view", f"{owner}/{repo_name}"],
            capture_output=True,
            text=True,
        )
        if result.stdout:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False


def _push_changes_to_repo() -> None:
    print("Pushing changes!")
    os.system(
        f"cd {REPO_NAME} && git add . && git commit -m 'Updated yaml from cli' && git push"
    )


def _create_yml(link: str, project_name: str) -> None:
    """Creates the yaml file and writes to it."""

    with open("action.yml") as f:
        reading = f.read()
    reading = reading.replace("YOURLINKHERE", link).replace(
        "Example-Project", project_name
    )

    print("Creating yaml file...")
    if not os.path.exists(f"{REPO_NAME}/.github/workflows/"):
        os.makedirs(f"{REPO_NAME}/.github/workflows/")
    with open(f"{REPO_NAME}/.github/workflows/build.yml", "w") as file:
        file.write(reading)


def create_and_clone_and_change_and_push_and_build(xcproj_link: str, project_name: str):
    if _check_repo_exists(USERNAME, REPO_NAME):
        print("Repo exists! Clone it!")

        if os.path.exists(REPO_NAME):
            overwrite = inquirer.confirm(
                f"Do you want to overwrite the current directory named {REPO_NAME}?",
                default=True,
            ).execute()
            if not overwrite:
                print("Aborted.")
                quit()

            print(f"Deleting {REPO_NAME} folder and cloning {USERNAME}/{REPO_NAME}!")
            shutil.rmtree(REPO_NAME)

        os.system(f"git clone https://github.com/{USERNAME}/{REPO_NAME}")
        print("Done cloning!")
    else:
        print("Creating repository...")

        if os.path.exists(REPO_NAME):
            overwrite = inquirer.confirm(
                f"Do you want to overwrite the current directory named {REPO_NAME}?"
            ).execute()
            if not overwrite:
                print("Aborted.")
                quit()

            print(f"Deleting {REPO_NAME} folder and creating {USERNAME}/{REPO_NAME}!")
            shutil.rmtree(REPO_NAME)

        subprocess.run(["gh", "repo", "create", REPO_NAME, "--private", "--clone"])

    _create_yml(xcproj_link, project_name)
    _push_changes_to_repo()

    inquirer.confirm("Build the repo?", default=True).execute()
    os.system(f'gh workflow run "Build iOS app" --repo {USERNAME}/{REPO_NAME}')
    print(
        f"Check out your build at https://github.com/{USERNAME}/{REPO_NAME}/actions and then click the topmost entry. Then scroll down to artifacts, and click the download icon next to your app."
    )


if __name__ == "__main__":
    create_and_clone_and_change_and_push_and_build("link", "project")
