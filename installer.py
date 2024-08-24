import os
import platform
import subprocess
import zipfile
import tarfile
import requests
from io import BytesIO
from pathlib import Path

GITHUB_REPO_URL = (
    "https://github.com/ThePloitZ/Snapify-Installer"  # Replace with your repo
)
SCRIPT_NAME = "installer.py"
LOCAL_SCRIPT_PATH = Path(__file__).resolve()


def download_adb(url, dest_folder):
    print("Downloading ADB...")
    response = requests.get(url)
    response.raise_for_status()

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    archive_path = os.path.join(dest_folder, "adb_tools")
    with open(archive_path, "wb") as file:
        file.write(response.content)

    print("Download complete.")
    return archive_path


def extract_archive(archive_path, dest_folder):
    print("Extracting ADB...")
    if archive_path.endswith(".zip"):
        with zipfile.ZipFile(archive_path, "r") as zip_ref:
            zip_ref.extractall(dest_folder)
    elif archive_path.endswith(".tar.xz"):
        with tarfile.open(archive_path, "r:xz") as tar_ref:
            tar_ref.extractall(dest_folder)
    else:
        raise ValueError("Unsupported archive format")
    print("Extraction complete.")


def add_to_path(adb_folder):
    adb_path = os.path.join(adb_folder, "platform-tools")

    if platform.system() == "Windows":
        os.environ["PATH"] += os.pathsep + adb_path
        print(f"ADB path added: {adb_path}")
    else:
        shell_profile = (
            os.path.expanduser("~/.bashrc")
            if platform.system() == "Linux"
            else os.path.expanduser("~/.zshrc")
        )
        with open(shell_profile, "a") as file:
            file.write(f'\nexport PATH="$PATH:{adb_path}"\n')
        print(f"ADB path added to {shell_profile}. Please restart your terminal.")


def verify_adb_installation():
    try:
        result = subprocess.run(
            ["adb", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            print("ADB installed successfully!")
            print(result.stdout.decode())
        else:
            print("ADB installation failed.")
            print(result.stderr.decode())
    except FileNotFoundError:
        print("ADB not found. Please ensure it's installed correctly.")


def update_script():
    print("Checking for script updates...")
    response = requests.get(f"{GITHUB_REPO_URL}/raw/main/{SCRIPT_NAME}")
    if response.status_code == 200:
        new_script_content = response.text
        with open(LOCAL_SCRIPT_PATH, "w") as script_file:
            script_file.write(new_script_content)
        print("Script updated successfully. Please re-run the script.")
        exit()
    else:
        print(f"Failed to update script. Status code: {response.status_code}")


def main():
    system = platform.system()
    dest_folder = os.path.expanduser("~/adb_install")

    # Update the script before proceeding
    update_script()

    if system == "Windows":
        url = (
            "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
        )
    elif system == "Darwin":  # macOS
        url = (
            "https://dl.google.com/android/repository/platform-tools-latest-darwin.zip"
        )
    elif system == "Linux":
        url = "https://dl.google.com/android/repository/platform-tools-latest-linux.zip"
    else:
        raise OSError("Unsupported operating system")

    try:
        archive_path = download_adb(url, dest_folder)
        extract_archive(archive_path, dest_folder)
        add_to_path(dest_folder)
        verify_adb_installation()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
