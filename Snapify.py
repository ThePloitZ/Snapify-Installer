import uiautomator2 as u2
from pystyle import *
import platform
import os
import subprocess
from time import sleep
from pathlib import Path
import shutil

# Initialize clear command as a global variable
clear = ""

banner = """
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣶⣶⣶⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀  Snapify v8
⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀  By unofficialdxnny & Seorex
⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀  #1 Snapscore Botter
⠀⠀⠀⢀⣀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⡀⠀⠀⠀             
⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠈⠙⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠋⠁⠀⠀
⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠀⠀
⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄
⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃
⠀⠀⠉⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⠉⠀⠀
⠀⠀⠀⠀⠈⠛⠛⠋⠙⠿⣿⣿⣿⣿⣿⣿⠿⠋⠙⠛⠛⠁⠀⠀⠀⠀
"""


def system_is():
    global clear
    # Detects the OS of the system it is running on
    os_type = platform.system()

    if os_type == "Windows":
        print(Colorate.Color(Colors.cyan, "Running on Windows", True))
        clear = "cls"
    elif os_type == "Linux":
        print(Colorate.Color(Colors.orange, "Running on Linux", True))
        clear = "clear"
    elif os_type == "Darwin":
        print(Colorate.Color(Colors.white, "Running on macOS", True))
        clear = "clear"
    else:
        print(f"What your PC smokin?\nGet a different OS!")


def adb_here():
    # Check if adb is installed
    try:
        # Attempt to run adb version to verify installation
        result = subprocess.run(
            ["adb", "version"], capture_output=True, text=True, check=True
        )
        print(Colorate.Color(Colors.green, f"ADB is installed:", True))
        print(Colorate.Color(Colors.yellow, result.stdout, True))
    except subprocess.CalledProcessError:
        print(Colorate.Color(Colors.red, "ADB command failed.", True))
        install_adb()
    except FileNotFoundError:
        print(
            Colorate.Color(
                Colors.red, "ADB is not installed or not found in the PATH.", True
            )
        )
        install_adb()


def install_adb():
    os_type = platform.system()

    if os_type == "Windows":
        print(
            Colorate.Color(
                Colors.yellow, "Attempting to install ADB on Windows...", True
            )
        )
        # Download the latest adb installer script from GitHub (you can customize the link)
        url = "https://dl.google.com/android/repository/platform-tools_r31.0.3-windows.zip"
        zip_path = Path("platform-tools.zip")
        extract_to = Path("platform-tools")
        # Download adb
        subprocess.run(
            [
                "powershell",
                "-Command",
                f"Invoke-WebRequest -Uri {url} -OutFile {zip_path}",
            ],
            check=True,
        )
        # Unzip
        subprocess.run(
            [
                "powershell",
                "-Command",
                f"Expand-Archive -Path {zip_path} -DestinationPath {extract_to}",
            ],
            check=True,
        )
        # Remove the zip file
        zip_path.unlink()

        # Move contents from platform-tools to CWD
        platform_tools_path = extract_to / "platform-tools"
        for item in platform_tools_path.iterdir():
            if item.is_file() or item.is_dir():
                shutil.move(str(item), str(Path.cwd() / item.name))

        # Add platform-tools to PATH for current session
        os.environ["PATH"] += os.pathsep + str(Path.cwd() / "platform-tools")

        # Clean up
        shutil.rmtree(extract_to)

    elif os_type == "Linux":
        print(
            Colorate.Color(Colors.yellow, "Attempting to install ADB on Linux...", True)
        )
        # Update package list and install adb
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "adb"], check=True)

        # Add adb to PATH if needed
        adb_path = subprocess.run(
            ["which", "adb"], capture_output=True, text=True, check=True
        ).stdout.strip()
        if adb_path:
            os.environ["PATH"] += os.pathsep + str(Path(adb_path).parent)

    elif os_type == "Darwin":
        print(
            Colorate.Color(Colors.yellow, "Attempting to install ADB on macOS...", True)
        )
        # Install adb using Homebrew
        subprocess.run(["brew", "install", "android-platform-tools"], check=True)

        # Add adb to PATH if needed
        adb_path = subprocess.run(
            ["which", "adb"], capture_output=True, text=True, check=True
        ).stdout.strip()
        if adb_path:
            os.environ["PATH"] += os.pathsep + str(Path(adb_path).parent)

    else:
        print(
            Colorate.Color(
                Colors.red, "Unsupported OS for automatic ADB installation.", True
            )
        )
        return

    # Verify adb installation
    try:
        result = subprocess.run(
            ["adb", "version"], capture_output=True, text=True, check=True
        )
        print(Colorate.Color(Colors.green, "ADB is installed:", True))
        print(Colorate.Color(Colors.yellow, result.stdout, True))
    except subprocess.CalledProcessError:
        print(Colorate.Color(Colors.red, "ADB command failed.", True))
    except FileNotFoundError:
        print(
            Colorate.Color(
                Colors.red, "ADB is not installed or not found in the PATH.", True
            )
        )


system_is()
os.system(clear)
print(Colorate.Color(Colors.yellow, banner, True))
adb_here()
