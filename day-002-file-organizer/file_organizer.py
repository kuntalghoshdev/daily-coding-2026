from pathlib import Path
import shutil
import json
from datetime import datetime


# ==========================================
# SMART FILE ORGANIZER
# ==========================================

APP_NAME = "SMART FILE ORGANIZER"
VERSION = "1.0"

LOG_FILE = "organization_log.json"


# ==========================================
# FILE CATEGORIES
# ==========================================

FILE_CATEGORIES = {
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp",
        ".webp", ".svg", ".ico", ".tiff", ".heic"
    ],

    "Documents": [
        ".pdf", ".doc", ".docx", ".txt", ".rtf",
        ".odt", ".md"
    ],

    "Spreadsheets": [
        ".xls", ".xlsx", ".csv", ".ods"
    ],

    "Presentations": [
        ".ppt", ".pptx", ".odp"
    ],

    "Music": [
        ".mp3", ".wav", ".flac", ".aac",
        ".ogg", ".m4a", ".wma"
    ],

    "Videos": [
        ".mp4", ".mkv", ".avi", ".mov",
        ".wmv", ".flv", ".webm", ".m4v"
    ],

    "Archives": [
        ".zip", ".rar", ".7z", ".tar",
        ".gz", ".bz2", ".xz"
    ],

    "Code": [
        ".py", ".js", ".ts", ".jsx", ".tsx",
        ".java", ".c", ".cpp", ".h", ".hpp",
        ".html", ".css", ".scss", ".php",
        ".go", ".rs", ".dart", ".sql",
        ".json", ".xml", ".yaml", ".yml"
    ],

    "Executables": [
        ".exe", ".msi", ".bat", ".cmd",
        ".sh", ".apk"
    ]
}


# ==========================================
# COLORS
# ==========================================

RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"


# ==========================================
# UI FUNCTIONS
# ==========================================

def clear_screen():
    print("\033[2J\033[H", end="")


def print_header():
    print(CYAN + "=" * 55 + RESET)
    print(CYAN + f"        {APP_NAME} 📁" + RESET)
    print(WHITE + f"                  Version {VERSION}" + RESET)
    print(CYAN + "=" * 55 + RESET)


def pause():
    input("\nPress Enter to continue...")


# ==========================================
# CATEGORY DETECTION
# ==========================================

def get_category(file_path):
    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Other"


# ==========================================
# SAFE FILE NAME
# ==========================================

def get_unique_path(destination):
    """
    Prevents overwriting files.

    Example:
    photo.jpg
    photo_1.jpg
    photo_2.jpg
    """

    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = (
            f"{destination.stem}_{counter}"
            f"{destination.suffix}"
        )

        new_path = destination.parent / new_name

        if not new_path.exists():
            return new_path

        counter += 1


# ==========================================
# FIND FILES
# ==========================================

def get_files(folder):
    files = []

    for item in folder.iterdir():

        # Ignore directories
        if item.is_dir():
            continue

        # Ignore hidden files
        if item.name.startswith("."):
            continue

        files.append(item)

    return files


# ==========================================
# PREVIEW ORGANIZATION
# ==========================================

def preview_files(folder):
    files = get_files(folder)

    if not files:
        print(YELLOW + "\nNo files found in this folder." + RESET)
        return

    print("\n" + BLUE + "PREVIEW" + RESET)
    print("-" * 55)

    for file in files:
        category = get_category(file)

        print(
            f"{file.name}"
            f"  →  "
            f"{category}/"
        )

    print("-" * 55)
    print(f"Total files: {len(files)}")


# ==========================================
# ORGANIZE FILES
# ==========================================

def organize_files(folder):
    files = get_files(folder)

    if not files:
        print(YELLOW + "\nNo files found." + RESET)
        return

    operations = []
    statistics = {}

    print("\n" + GREEN + "Organizing files..." + RESET)
    print("-" * 55)

    for file in files:

        category = get_category(file)

        category_folder = folder / category

        category_folder.mkdir(exist_ok=True)

        destination = category_folder / file.name

        # Prevent overwriting
        destination = get_unique_path(destination)

        try:
            shutil.move(str(file), str(destination))

            operations.append({
                "source": str(file),
                "destination": str(destination)
            })

            statistics[category] = (
                statistics.get(category, 0) + 1
            )

            print(
                GREEN
                + f"✓ {file.name}"
                + RESET
                + f" → {category}/"
            )

        except Exception as error:
            print(
                RED
                + f"✗ Failed: {file.name}"
                + RESET
            )

            print(f"  Error: {error}")

    save_log(operations)

    print("\n" + GREEN + "=" * 55 + RESET)
    print(GREEN + "Organization completed!" + RESET)
    print(GREEN + "=" * 55 + RESET)

    print_statistics(statistics)


# ==========================================
# STATISTICS
# ==========================================

def print_statistics(statistics):

    total = sum(statistics.values())

    print("\n📊 Organization Statistics")
    print("-" * 40)

    for category, count in sorted(statistics.items()):
        print(f"{category:<20} : {count}")

    print("-" * 40)
    print(f"{'Total files':<20} : {total}")


# ==========================================
# SAVE LOG
# ==========================================

def save_log(operations):

    log_data = {
        "timestamp": datetime.now().isoformat(),
        "operations": operations
    }

    try:
        with open(LOG_FILE, "w", encoding="utf-8") as file:
            json.dump(
                log_data,
                file,
                indent=4
            )

    except Exception as error:
        print(
            RED
            + f"Could not save log: {error}"
            + RESET
        )


# ==========================================
# LOAD LOG
# ==========================================

def load_log():

    log_path = Path(LOG_FILE)

    if not log_path.exists():
        return None

    try:
        with open(
            log_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:
        return None


# ==========================================
# UNDO LAST ORGANIZATION
# ==========================================

def undo_last_organization():

    log_data = load_log()

    if not log_data:
        print(
            YELLOW
            + "\nNo organization history found."
            + RESET
        )
        return

    operations = log_data.get("operations", [])

    if not operations:
        print(
            YELLOW
            + "\nNo operations to undo."
            + RESET
        )
        return

    print("\n" + MAGENTA + "UNDO LAST ORGANIZATION" + RESET)
    print("-" * 55)

    restored = 0

    for operation in reversed(operations):

        source = Path(operation["source"])
        destination = Path(operation["destination"])

        if not destination.exists():
            continue

        try:
            source.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            restored_path = get_unique_path(source)

            shutil.move(
                str(destination),
                str(restored_path)
            )

            print(
                GREEN
                + f"✓ Restored: {restored_path.name}"
                + RESET
            )

            restored += 1

        except Exception as error:

            print(
                RED
                + f"✗ Could not restore {destination.name}"
                + RESET
            )

            print(f"  Error: {error}")

    print("\n" + GREEN + f"Restored files: {restored}" + RESET)

    # Remove log after successful undo
    try:
        Path(LOG_FILE).unlink()
    except FileNotFoundError:
        pass


# ==========================================
# FOLDER SELECTION
# ==========================================

def choose_folder():

    print("\nEnter the folder you want to organize.")
    print("Example:")
    print(r"C:\Users\YourName\Downloads")

    folder_input = input("\nFolder path: ").strip()

    # Remove quotes if user pasted a quoted path
    folder_input = folder_input.strip('"').strip("'")

    folder = Path(folder_input).expanduser()

    if not folder.exists():
        print(
            RED
            + "\n❌ Folder does not exist."
            + RESET
        )
        return None

    if not folder.is_dir():
        print(
            RED
            + "\n❌ The selected path is not a folder."
            + RESET
        )
        return None

    return folder


# ==========================================
# MENU
# ==========================================

def main():

    while True:

        clear_screen()
        print_header()

        print("\n1. 📁 Organize Folder")
        print("2. 👀 Preview Organization")
        print("3. 🔄 Undo Last Organization")
        print("4. 🚪 Exit")

        choice = input("\nChoose an option: ").strip()

        # ------------------------------
        # ORGANIZE
        # ------------------------------

        if choice == "1":

            folder = choose_folder()

            if folder:

                print(
                    "\n" + YELLOW
                    + "⚠️ You are about to organize:"
                    + RESET
                )

                print(folder)

                confirm = input(
                    "\nContinue? (y/n): "
                ).lower().strip()

                if confirm == "y":

                    organize_files(folder)

                else:

                    print(
                        YELLOW
                        + "\nOperation cancelled."
                        + RESET
                    )

                pause()

        # ------------------------------
        # PREVIEW
        # ------------------------------

        elif choice == "2":

            folder = choose_folder()

            if folder:
                preview_files(folder)

            pause()

        # ------------------------------
        # UNDO
        # ------------------------------

        elif choice == "3":

            undo_last_organization()

            pause()

        # ------------------------------
        # EXIT
        # ------------------------------

        elif choice == "4":

            print(
                GREEN
                + "\nThanks for using Smart File Organizer! 👋"
                + RESET
            )

            break

        else:

            print(
                RED
                + "\n❌ Invalid option."
                + RESET
            )

            pause()


# ==========================================
# PROGRAM START
# ==========================================

if __name__ == "__main__":
    main()