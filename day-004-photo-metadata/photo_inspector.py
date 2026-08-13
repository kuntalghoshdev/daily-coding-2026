from PIL import Image, ExifTags
from pathlib import Path
import json
import os
import shutil
from datetime import datetime


APP_NAME = "PHOTO METADATA INSPECTOR"
VERSION = "1.0"

REPORT_FILE = "photo_report.json"

RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"


# ============================================================
# UI
# ============================================================

def clear_screen():
    print("\033[2J\033[H", end="")


def header():
    print(CYAN + "=" * 65 + RESET)
    print(CYAN + "              📸 PHOTO METADATA INSPECTOR" + RESET)
    print(CYAN + f"                         Version {VERSION}" + RESET)
    print(CYAN + "=" * 65 + RESET)


def pause():
    input("\nPress Enter to continue...")


# ============================================================
# FILE SIZE
# ============================================================

def format_size(size):

    units = ["B", "KB", "MB", "GB"]

    value = float(size)

    for unit in units:

        if value < 1024:
            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} TB"


# ============================================================
# SAFE VALUE CONVERSION
# ============================================================

def safe_value(value):

    try:

        if hasattr(value, "numerator") and hasattr(value, "denominator"):

            if value.denominator != 0:
                return round(
                    value.numerator / value.denominator,
                    4
                )

        return str(value)

    except Exception:

        return str(value)


# ============================================================
# EXIF EXTRACTION
# ============================================================

def extract_exif(image):

    exif_data = {}

    try:

        raw_exif = image.getexif()

        if not raw_exif:
            return exif_data

        for tag_id, value in raw_exif.items():

            tag_name = ExifTags.TAGS.get(
                tag_id,
                str(tag_id)
            )

            exif_data[tag_name] = safe_value(value)

    except Exception:

        pass

    return exif_data


# ============================================================
# GPS EXTRACTION
# ============================================================

def extract_gps(image):

    try:

        exif = image.getexif()

        gps_info = exif.get_ifd(
            ExifTags.IFD.GPSInfo
        )

        if not gps_info:
            return None

        readable = {}

        for tag_id, value in gps_info.items():

            tag_name = ExifTags.GPSTAGS.get(
                tag_id,
                str(tag_id)
            )

            readable[tag_name] = safe_value(value)

        return readable

    except Exception:

        return None


# ============================================================
# CAMERA INFORMATION
# ============================================================

def get_camera_info(exif):

    return {
        "make": exif.get(
            "Make",
            "Not available"
        ),

        "model": exif.get(
            "Model",
            "Not available"
        ),

        "lens": exif.get(
            "LensModel",
            "Not available"
        )
    }


# ============================================================
# PHOTO ANALYSIS
# ============================================================

def analyze_photo(file_path):

    try:

        image = Image.open(file_path)

        exif = extract_exif(image)

        gps = extract_gps(image)

        file_size = os.path.getsize(file_path)

        width, height = image.size

        megapixels = (
            width * height
        ) / 1_000_000

        analysis = {

            "file": {
                "name": file_path.name,
                "path": str(file_path),
                "size": format_size(file_size),
                "size_bytes": file_size
            },

            "image": {
                "format": image.format,
                "width": width,
                "height": height,
                "megapixels": round(
                    megapixels,
                    2
                ),
                "mode": image.mode
            },

            "camera": get_camera_info(exif),

            "exif": exif,

            "gps": gps
        }

        image.close()

        return analysis

    except Exception as error:

        print(
            RED
            + f"\n❌ Could not read image: {error}"
            + RESET
        )

        return None


# ============================================================
# DISPLAY BASIC INFORMATION
# ============================================================

def display_basic_info(data):

    print(
        "\n"
        + BLUE
        + "🖼️ IMAGE INFORMATION"
        + RESET
    )

    print("-" * 65)

    image = data["image"]
    file_data = data["file"]

    print(
        f"File             : "
        f"{file_data['name']}"
    )

    print(
        f"Format           : "
        f"{image['format']}"
    )

    print(
        f"Dimensions       : "
        f"{image['width']} × {image['height']}"
    )

    print(
        f"Megapixels       : "
        f"{image['megapixels']} MP"
    )

    print(
        f"Color Mode       : "
        f"{image['mode']}"
    )

    print(
        f"File Size        : "
        f"{file_data['size']}"
    )


# ============================================================
# DISPLAY CAMERA INFORMATION
# ============================================================

def display_camera(data):

    print(
        "\n"
        + MAGENTA
        + "📷 CAMERA INFORMATION"
        + RESET
    )

    print("-" * 65)

    camera = data["camera"]

    print(
        f"Make             : "
        f"{camera['make']}"
    )

    print(
        f"Model            : "
        f"{camera['model']}"
    )

    print(
        f"Lens             : "
        f"{camera['lens']}"
    )


# ============================================================
# DISPLAY PHOTOGRAPHY SETTINGS
# ============================================================

def display_settings(data):

    exif = data["exif"]

    print(
        "\n"
        + YELLOW
        + "⚙️ PHOTOGRAPHY SETTINGS"
        + RESET
    )

    print("-" * 65)

    print(
        f"Date Taken       : "
        f"{exif.get('DateTimeOriginal', 'Not available')}"
    )

    print(
        f"ISO              : "
        f"{exif.get('ISOSpeedRatings', 'Not available')}"
    )

    print(
        f"Aperture         : "
        f"{exif.get('FNumber', 'Not available')}"
    )

    print(
        f"Shutter Speed    : "
        f"{exif.get('ExposureTime', 'Not available')}"
    )

    print(
        f"Focal Length     : "
        f"{exif.get('FocalLength', 'Not available')}"
    )

    print(
        f"Flash            : "
        f"{exif.get('Flash', 'Not available')}"
    )


# ============================================================
# DISPLAY GPS
# ============================================================

def display_gps(data):

    print(
        "\n"
        + GREEN
        + "📍 GPS INFORMATION"
        + RESET
    )

    print("-" * 65)

    gps = data.get("gps")

    if not gps:

        print(
            "No GPS metadata found."
        )

        return

    for key, value in gps.items():

        print(
            f"{key:<20}: {value}"
        )


# ============================================================
# EXPORT JSON
# ============================================================

def export_report(data):

    try:

        report = {
            "generated_at":
                datetime.now().isoformat(),

            "photo_analysis":
                data
        }

        with open(
            REPORT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            GREEN
            + f"\n✅ Report saved to {REPORT_FILE}"
            + RESET
        )

    except Exception as error:

        print(
            RED
            + "\n❌ Failed to export report."
            + RESET
        )

        print(error)


# ============================================================
# REMOVE EXIF
# ============================================================

def remove_exif(file_path):

    try:

        image = Image.open(file_path)

        cleaned_image = Image.new(
            image.mode,
            image.size
        )

        cleaned_image.putdata(
            list(image.get_flattened_data())
        )

        output_path = (
            file_path.parent
            / f"{file_path.stem}_clean"
            f"{file_path.suffix}"
        )

        cleaned_image.save(
            output_path,
            format=image.format
        )

        image.close()
        cleaned_image.close()

        print(
            GREEN
            + "\n✅ EXIF metadata removed."
            + RESET
        )

        print(
            f"Clean image: {output_path}"
        )

    except Exception as error:

        print(
            RED
            + "\n❌ Could not remove metadata."
            + RESET
        )

        print(error)


# ============================================================
# FIND IMAGE
# ============================================================

def choose_image():

    path_input = input(
        "\nEnter image path: "
    ).strip()

    path_input = (
        path_input
        .strip('"')
        .strip("'")
    )

    path = Path(path_input)

    if not path.exists():

        print(
            RED
            + "\n❌ File does not exist."
            + RESET
        )

        return None

    if not path.is_file():

        print(
            RED
            + "\n❌ Path is not a file."
            + RESET
        )

        return None

    supported = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".tiff",
        ".bmp"
    }

    if path.suffix.lower() not in supported:

        print(
            RED
            + "\n❌ Unsupported image format."
            + RESET
        )

        return None

    return path


# ============================================================
# INSPECT PHOTO
# ============================================================

def inspect_photo():

    file_path = choose_image()

    if not file_path:
        return

    print(
        "\n"
        + YELLOW
        + "Analyzing image..."
        + RESET
    )

    data = analyze_photo(file_path)

    if not data:
        return

    clear_screen()
    header()

    display_basic_info(data)

    display_camera(data)

    display_settings(data)

    display_gps(data)

    export = input(
        "\nExport report as JSON? (y/n): "
    ).strip().lower()

    if export == "y":

        export_report(data)


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        clear_screen()
        header()

        print("\n1. 🔍 Inspect Photo")
        print("2. 🧹 Remove EXIF Metadata")
        print("3. 🚪 Exit")

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":

            inspect_photo()
            pause()

        elif choice == "2":

            file_path = choose_image()

            if file_path:

                print(
                    "\n"
                    + YELLOW
                    + "⚠️ This creates a new cleaned copy."
                    + RESET
                )

                confirm = input(
                    "Continue? (y/n): "
                ).strip().lower()

                if confirm == "y":

                    remove_exif(file_path)

            pause()

        elif choice == "3":

            print(
                GREEN
                + "\nThanks for using Photo Metadata Inspector! 👋"
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


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()