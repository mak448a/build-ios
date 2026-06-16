from InquirerPy import inquirer
import dropbox.exceptions

from dbx_integration import upload_file, dropbox
from ipa_editor import replace_pck
from gh_integration import create_and_clone_and_change_and_push_and_build

import shutil
import os
import platform
import sys
import dotenv
import uuid


dotenv.load_dotenv()
IPA = os.getenv("IPA")


def edit_ipa() -> None:
    invalid: bool = False

    while True:
        if not IPA or invalid:
            ipa_path = inquirer.text("Enter path to IPA file to edit:").execute()
        else:
            ipa_path = IPA

        # Check if files exist
        if os.path.exists(ipa_path) and os.path.exists(f"{ipa_path[0:-4]}.pck"):
            break
        else:
            print(
                f"Invalid files! Either '{ipa_path[0:-4]}.pck' and/or {ipa_path} doesn't/don't exist!"
                f"{"\nYour IPA entry in '.env' is faulty!" if IPA and not invalid else ''}"
            )
            invalid = True

    print("Valid files! Replacing PCK file with new one! This may take a minute...")
    replace_pck(ipa_path)
    print("Success!")


def create_new_ipa() -> str:
    print("Make sure you have enough storage on Dropbox! Otherwise, exit now.")

    while True:
        path = inquirer.text(message="Enter path to folder of XCodeProject:").execute()
        try:
            print("Zipping your project...")
            shutil.make_archive("tempxcodeproject", "zip", path)
            print("Zipped! Now uploading to Dropbox. THIS MAY TAKE A LONG TIME!!!")

            link = upload_file("tempxcodeproject.zip", f"/{uuid.uuid1()}.zip")
            link = link[0:-1] + "1"
            break
        except FileNotFoundError:
            print("Invalid folder.")
            continue
        except dropbox.exceptions.ApiError:
            print("There was an API error. Perhaps try deleting the previous upload from dropbox?")
            quit()

    # Cleanup
    os.remove("tempxcodeproject.zip")

    # Return the link to the download
    return link


if __name__ == "__main__":
    version = platform.python_version().split(".")
    if version[0] != 3:
        print("Python is not 3.x!")
        sys.exit(1)
    elif int(version[1]) >= 12:
        print("Python version 3.12 or above, continuing!")
    else:
        print("Python version unsupported! Make sure to use Python 3.12 or above!")

    mode = inquirer.select(
        message="Pick a mode",
        choices=["Edit IPA", "Create new IPA"],
    ).execute()

    if mode == "Edit IPA":
        edit_ipa()
        quit()
    elif mode == "Create new IPA":
        link = create_new_ipa()

        confirmation = inquirer.confirm(
            "Do you want to continue to uploading to GitHub? If no, quit.", default=True
        ).execute()
        if not confirmation:
            print("Quitting! You can manually build it later on your GitHub repo.")
            quit()

        print("Proceeding to the GitHub step!")

        if IPA:
            create_and_clone_and_change_and_push_and_build(link, IPA[0:-4])
        else:
            proj_name = inquirer.text("What's the name of the ipa file you exported in Godot Engine?").execute()
            create_and_clone_and_change_and_push_and_build(link, proj_name)
    else:
        print("Invalid choice!")
