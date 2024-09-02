import platform
import os
import subprocess
from pathlib import Path
import shutil
import keyboard  # For capturing keyboard events
from pystyle import Colorate, Colors

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
⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃
⠀⠀⠉⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⠉⠀⠀
⠀⠀⠀⠀⠈⠛⠛⠋⠙⠿⣿⣿⣿⣿⣿⣿⠿⠋⠙⠛⠛⠁⠀⠀⠀⠀
"""

menu_items = ["[1] Android", "[2] Emulator", "[3] WEB", "[4] Exit"]


def system_is():
    global clear
    os_type = platform.system()

    if os_type == "Windows":
        clear = "cls"
    elif os_type == "Linux":
        clear = "clear"
    elif os_type == "Darwin":
        clear = "clear"
    else:
        print(f"What your PC smokin?\nGet a different OS!")


def adb_here():
    try:
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
        url = "https://dl.google.com/android/repository/platform-tools_r31.0.3-windows.zip"
        zip_path = Path("platform-tools.zip")
        extract_to = Path("platform-tools")

        subprocess.run(
            [
                "powershell",
                "-Command",
                f"Invoke-WebRequest -Uri {url} -OutFile {zip_path}",
            ],
            check=True,
        )
        subprocess.run(
            [
                "powershell",
                "-Command",
                f"Expand-Archive -Path {zip_path} -DestinationPath {extract_to}",
            ],
            check=True,
        )
        zip_path.unlink()

        platform_tools_path = extract_to / "platform-tools"
        for item in platform_tools_path.iterdir():
            if item.is_file() or item.is_dir():
                shutil.move(str(item), str(Path.cwd() / item.name))

        os.environ["PATH"] += os.pathsep + str(Path.cwd() / "platform-tools")
        shutil.rmtree(extract_to)

    elif os_type == "Linux":
        print(
            Colorate.Color(Colors.yellow, "Attempting to install ADB on Linux...", True)
        )
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "adb"], check=True)

        adb_path = subprocess.run(
            ["which", "adb"], capture_output=True, text=True, check=True
        ).stdout.strip()
        if adb_path:
            os.environ["PATH"] += os.pathsep + str(Path(adb_path).parent)

    elif os_type == "Darwin":
        print(
            Colorate.Color(Colors.yellow, "Attempting to install ADB on macOS...", True)
        )
        subprocess.run(["brew", "install", "android-platform-tools"], check=True)

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


def print_menu(selected_index):
    os.system(clear)
    print(Colorate.Color(Colors.yellow, banner, True))
    for index, item in enumerate(menu_items):
        if index == selected_index:
            print(Colorate.Color(Colors.green, item, True))
        else:
            print(Colorate.Color(Colors.yellow, item, True))


def handle_choice(index):
    if index == 0:
        print("Android option selected.")
    elif index == 1:
        print("Emulator option selected.")
    elif index == 2:
        print("WEB option selected.")
    elif index == 3:
        print("Exiting...")
        exit()


def menu_navigation():
    selected_index = 0
    while True:
        print_menu(selected_index)
        event = keyboard.read_event()

        if event.name == "up" and selected_index > 0:
            selected_index -= 1
        elif event.name == "down" and selected_index < len(menu_items) - 1:
            selected_index += 1
        elif event.name == "enter":
            handle_choice(selected_index)
        elif event.name == "esc":
            print("Exiting...")
            exit()


system_is()
os.system(clear)
print(Colorate.Color(Colors.yellow, banner, True))
adb_here()

menu_navigation()
