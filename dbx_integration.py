import dropbox
from dotenv import load_dotenv
import os


load_dotenv()

# Your Dropbox API access token
ACCESS_TOKEN = os.getenv("TOKEN")

# Initialize the Dropbox client
dbx = dropbox.Dropbox(ACCESS_TOKEN)

print(
    "Get your token at https://www.dropbox.com/developers/apps and ensure you have the necessary permissions ticked on!"
)


def upload_file(file_path, dropbox_path):
    with open(file_path, "rb") as f:
        dbx.files_upload(f.read(), dropbox_path)

    print(f"File {file_path} uploaded to {dropbox_path} successfully.")

    # Generate a shared link
    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_path)

    return shared_link_metadata.url


if __name__ == "__main__":
    upload_file("requirements.txt", "/requirements.txt")
