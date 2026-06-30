from dotenv import load_dotenv
import subprocess
import shutil
import stat
import os
import inquirer as inq


load_dotenv()
GH_USERNAME = os.getenv("GH_USERNAME")
REPO_NAME = os.getenv("REPO_NAME")


if not GH_USERNAME or not REPO_NAME:
    GH_USERNAME = inq.prompt([inq.Text("name", message="What's your GitHub username?")]).get("name")  # type: ignore
    REPO_NAME = inq.prompt(
        [
            inq.Text(
                "repo",
                message="What's the name of the repo that you want to store your repo builder in? (contents will be overwritten)",
            )
        ]
    ).get("repo")  # type: ignore
    print(REPO_NAME, GH_USERNAME)

    # Make type checker stop complaining
    assert REPO_NAME is not None
    assert GH_USERNAME is not None

    print(GH_USERNAME, REPO_NAME)


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
        f'cd {REPO_NAME} && git branch -M main && git add . && git commit -m "Updated yaml from cli" && git push -u origin main'
    )


def _create_yml(link: str, project_name: str) -> None:
    """Creates the yaml file and writes to it."""

    with open("action.yml") as f:
        reading = f.read()
    reading = reading.replace("YOURLINKHERE", link).replace("Example-Project", project_name)

    print("Creating yaml file...")
    if not os.path.exists(f"{REPO_NAME}/.github/workflows/"):
        os.makedirs(f"{REPO_NAME}/.github/workflows/")
    with open(f"{REPO_NAME}/.github/workflows/build.yml", "w") as file:
        file.write(reading)


def change_permission(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def create_and_clone_and_change_and_push_and_build(xcproj_link: str, project_name: str):
    # Satisfy type checker
    assert isinstance(REPO_NAME, str)
    assert isinstance(GH_USERNAME, str)

    if _check_repo_exists(GH_USERNAME, REPO_NAME):
        print("Repo exists! Clone it!")

        if os.path.exists(REPO_NAME):
            overwrite = inq.prompt(
                [inq.Confirm("ans", message=f"Do you want to overwrite the current directory named {REPO_NAME}?")]
            ).get("ans")  # type: ignore

            if not overwrite:
                print("Aborted.")
                quit()

            print(f"Deleting {REPO_NAME} folder and cloning {GH_USERNAME}/{REPO_NAME}!")

            shutil.rmtree(REPO_NAME, onexc=change_permission)

        os.system(f"git clone https://github.com/{GH_USERNAME}/{REPO_NAME}")
        print("Done cloning!")
    else:
        print("Creating repository...")

        if os.path.exists(REPO_NAME):
            overwrite = inq.prompt(
                [inq.Confirm("ans", message=f"Do you want to overwrite the current directory named {REPO_NAME}?")]
            ).get("ans")  # type: ignore

            if not overwrite:
                print("Aborted.")
                quit()

            print(f"Deleting {REPO_NAME} folder and creating {GH_USERNAME}/{REPO_NAME}!")
            shutil.rmtree(REPO_NAME)

        subprocess.run(["gh", "repo", "create", REPO_NAME, "--private", "--clone"])

    _create_yml(xcproj_link, project_name)
    _push_changes_to_repo()

    inq.prompt(
        [inq.Confirm("ans", message=f"Building the repo! Press CTRL+C to cancel")], raise_keyboard_interrupt=True
    ).get("ans")  # type: ignore

    os.system(f'gh workflow run "Build iOS app" --repo {GH_USERNAME}/{REPO_NAME}')
    print(
        f"Check out your build at https://github.com/{GH_USERNAME}/{REPO_NAME}/actions and then click the topmost entry. Then scroll down to artifacts, and click the download icon next to your app."
    )


if __name__ == "__main__":
    create_and_clone_and_change_and_push_and_build("link", "project")
