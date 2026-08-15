import urllib.request
import urllib.error
import json
import csv
import time
from datetime import datetime
from pathlib import Path


# ============================================================
# SITEWATCH
# Website Uptime Monitor
# ============================================================

APP_NAME = "SITEWATCH"
VERSION = "1.0"

WEBSITES_FILE = "websites.json"
JSON_REPORT = "uptime_report.json"
CSV_REPORT = "uptime_report.csv"

TIMEOUT = 10


# ============================================================
# COLORS
# ============================================================

RESET = "\033[0m"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"


# ============================================================
# UI
# ============================================================

def clear_screen():
    print("\033[2J\033[H", end="")


def header():

    print(CYAN + "=" * 70 + RESET)

    print(
        CYAN
        + "                    🌐 SITEWATCH"
        + RESET
    )

    print(
        WHITE
        + "                 Website Uptime Monitor"
        + RESET
    )

    print(
        CYAN
        + f"                      Version {VERSION}"
        + RESET
    )

    print(CYAN + "=" * 70 + RESET)


def pause():

    input("\nPress Enter to continue...")


# ============================================================
# URL NORMALIZATION
# ============================================================

def normalize_url(url):

    url = url.strip()

    if not url:
        return None

    if not url.startswith(
        ("http://", "https://")
    ):

        url = "https://" + url

    return url


# ============================================================
# LOAD WEBSITE LIST
# ============================================================

def load_websites():

    path = Path(WEBSITES_FILE)

    if not path.exists():

        return []

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):

                return data

    except Exception:

        pass

    return []


# ============================================================
# SAVE WEBSITE LIST
# ============================================================

def save_websites(websites):

    try:

        with open(
            WEBSITES_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                websites,
                file,
                indent=4
            )

        return True

    except Exception as error:

        print(
            RED
            + f"\n❌ Could not save websites: {error}"
            + RESET
        )

        return False


# ============================================================
# ADD WEBSITE
# ============================================================

def add_website():

    url = input(
        "\nEnter website URL: "
    )

    url = normalize_url(url)

    if not url:

        print(
            RED
            + "\n❌ Invalid URL."
            + RESET
        )

        return

    websites = load_websites()

    if url in websites:

        print(
            YELLOW
            + "\n⚠️ Website already exists."
            + RESET
        )

        return

    websites.append(url)

    if save_websites(websites):

        print(
            GREEN
            + f"\n✅ Added: {url}"
            + RESET
        )


# ============================================================
# REMOVE WEBSITE
# ============================================================

def remove_website():

    websites = load_websites()

    if not websites:

        print(
            YELLOW
            + "\nNo websites saved."
            + RESET
        )

        return

    print("\nSaved Websites:")

    for index, url in enumerate(
        websites,
        start=1
    ):

        print(
            f"{index}. {url}"
        )

    try:

        choice = int(
            input(
                "\nEnter number to remove: "
            )
        )

        if choice < 1 or choice > len(websites):

            raise ValueError

        removed = websites.pop(
            choice - 1
        )

        save_websites(websites)

        print(
            GREEN
            + f"\n✅ Removed: {removed}"
            + RESET
        )

    except ValueError:

        print(
            RED
            + "\n❌ Invalid selection."
            + RESET
        )


# ============================================================
# CHECK WEBSITE
# ============================================================

def check_website(url):

    start_time = time.perf_counter()

    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "User-Agent":
                "SiteWatch/1.0"
        }
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=TIMEOUT
        ) as response:

            end_time = time.perf_counter()

            response_time = (
                end_time - start_time
            ) * 1000

            status_code = response.status

            if status_code < 400:

                if response_time < 500:
                    status = "ONLINE"

                elif response_time < 1500:
                    status = "SLOW"

                else:
                    status = "VERY SLOW"

            else:

                status = "ERROR"

            return {
                "url": url,
                "status": status,
                "status_code": status_code,
                "response_time_ms":
                    round(response_time, 2),
                "timestamp":
                    datetime.now().isoformat(),
                "error": None
            }

    except urllib.error.HTTPError as error:

        end_time = time.perf_counter()

        response_time = (
            end_time - start_time
        ) * 1000

        return {
            "url": url,
            "status": "ERROR",
            "status_code": error.code,
            "response_time_ms":
                round(response_time, 2),
            "timestamp":
                datetime.now().isoformat(),
            "error":
                str(error)
        }

    except urllib.error.URLError as error:

        return {
            "url": url,
            "status": "OFFLINE",
            "status_code": None,
            "response_time_ms": None,
            "timestamp":
                datetime.now().isoformat(),
            "error":
                str(error.reason)
        }

    except TimeoutError:

        return {
            "url": url,
            "status": "TIMEOUT",
            "status_code": None,
            "response_time_ms": None,
            "timestamp":
                datetime.now().isoformat(),
            "error":
                "Request timed out"
        }

    except Exception as error:

        return {
            "url": url,
            "status": "ERROR",
            "status_code": None,
            "response_time_ms": None,
            "timestamp":
                datetime.now().isoformat(),
            "error":
                str(error)
        }


# ============================================================
# STATUS ICON
# ============================================================

def status_display(status):

    if status == "ONLINE":

        return (
            GREEN
            + "🟢 ONLINE"
            + RESET
        )

    if status == "SLOW":

        return (
            YELLOW
            + "🟡 SLOW"
            + RESET
        )

    if status == "VERY SLOW":

        return (
            YELLOW
            + "🟠 VERY SLOW"
            + RESET
        )

    if status == "TIMEOUT":

        return (
            RED
            + "⏱️ TIMEOUT"
            + RESET
        )

    return (
        RED
        + "🔴 OFFLINE"
        + RESET
    )


# ============================================================
# CHECK ALL WEBSITES
# ============================================================

def check_all():

    websites = load_websites()

    if not websites:

        print(
            YELLOW
            + "\nNo websites configured."
            + RESET
        )

        print(
            "Use option 1 to add websites."
        )

        return []

    results = []

    print(
        "\n"
        + CYAN
        + "Checking websites..."
        + RESET
    )

    print("-" * 70)

    for url in websites:

        print(
            f"Checking {url}..."
        )

        result = check_website(url)

        results.append(result)

    display_results(results)

    return results


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(results):

    print("\n")

    print(
        BLUE
        + "WEBSITE STATUS"
        + RESET
    )

    print("-" * 70)

    print(
        f"{'Website':<35}"
        f"{'Status':<15}"
        f"{'Response':<15}"
    )

    print("-" * 70)

    for result in results:

        url = result["url"]

        if len(url) > 33:

            display_url = (
                url[:30]
                + "..."
            )

        else:

            display_url = url

        status = status_display(
            result["status"]
        )

        response = result[
            "response_time_ms"
        ]

        if response is None:

            response_text = "---"

        else:

            response_text = (
                f"{response} ms"
            )

        print(
            f"{display_url:<35}"
            f"{status:<25}"
            f"{response_text:<15}"
        )

    print("-" * 70)

    print_summary(results)


# ============================================================
# SUMMARY
# ============================================================

def print_summary(results):

    total = len(results)

    online = sum(
        1
        for result in results
        if result["status"] == "ONLINE"
    )

    slow = sum(
        1
        for result in results
        if result["status"] in (
            "SLOW",
            "VERY SLOW"
        )
    )

    offline = sum(
        1
        for result in results
        if result["status"] in (
            "OFFLINE",
            "TIMEOUT",
            "ERROR"
        )
    )

    response_times = [
        result["response_time_ms"]
        for result in results
        if result["response_time_ms"]
        is not None
    ]

    if response_times:

        average = (
            sum(response_times)
            / len(response_times)
        )

    else:

        average = 0

    print(
        f"\nChecked : {total} websites"
    )

    print(
        GREEN
        + f"Online  : {online}"
        + RESET
    )

    print(
        YELLOW
        + f"Slow    : {slow}"
        + RESET
    )

    print(
        RED
        + f"Offline : {offline}"
        + RESET
    )

    print(
        f"Average response time: "
        f"{average:.2f} ms"
    )


# ============================================================
# SAVE JSON REPORT
# ============================================================

def save_json_report(results):

    report = {

        "generated_at":
            datetime.now().isoformat(),

        "total_websites":
            len(results),

        "results":
            results
    }

    try:

        with open(
            JSON_REPORT,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        print(
            GREEN
            + f"\n✅ JSON report saved: "
            + JSON_REPORT
            + RESET
        )

    except Exception as error:

        print(
            RED
            + "\n❌ Could not save JSON report."
            + RESET
        )

        print(error)


# ============================================================
# SAVE CSV REPORT
# ============================================================

def save_csv_report(results):

    try:

        with open(
            CSV_REPORT,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "url",
                    "status",
                    "status_code",
                    "response_time_ms",
                    "timestamp",
                    "error"
                ]
            )

            writer.writeheader()

            writer.writerows(results)

        print(
            GREEN
            + f"✅ CSV report saved: "
            + CSV_REPORT
            + RESET
        )

    except Exception as error:

        print(
            RED
            + "\n❌ Could not save CSV report."
            + RESET
        )

        print(error)


# ============================================================
# SINGLE WEBSITE
# ============================================================

def check_single():

    url = input(
        "\nEnter website URL: "
    )

    url = normalize_url(url)

    if not url:

        print(
            RED
            + "\n❌ Invalid URL."
            + RESET
        )

        return

    print(
        "\n"
        + YELLOW
        + "Checking..."
        + RESET
    )

    result = check_website(url)

    display_results([result])


# ============================================================
# CONTINUOUS MONITOR
# ============================================================

def continuous_monitor():

    websites = load_websites()

    if not websites:

        print(
            YELLOW
            + "\nNo websites configured."
            + RESET
        )

        return

    try:

        interval = int(
            input(
                "\nCheck interval in seconds: "
            )
        )

        if interval < 5:

            print(
                YELLOW
                + "\nMinimum interval is 5 seconds."
                + RESET
            )

            return

    except ValueError:

        print(
            RED
            + "\n❌ Invalid interval."
            + RESET
        )

        return

    print(
        "\n"
        + GREEN
        + "Monitoring started."
        + RESET
    )

    print(
        YELLOW
        + "Press Ctrl+C to stop."
        + RESET
    )

    try:

        while True:

            clear_screen()

            header()

            results = check_all()

            print(
                "\nNext check in "
                f"{interval} seconds..."
            )

            time.sleep(interval)

    except KeyboardInterrupt:

        print(
            "\n"
            + GREEN
            + "\nMonitoring stopped."
            + RESET
        )


# ============================================================
# REPORT MENU
# ============================================================

def generate_report():

    results = check_all()

    if not results:

        return

    print(
        "\n"
        + CYAN
        + "Export report?"
        + RESET
    )

    print("1. JSON")
    print("2. CSV")
    print("3. Both")
    print("4. Cancel")

    choice = input(
        "\nChoose: "
    ).strip()

    if choice == "1":

        save_json_report(results)

    elif choice == "2":

        save_csv_report(results)

    elif choice == "3":

        save_json_report(results)
        save_csv_report(results)

    elif choice == "4":

        print(
            "\nExport cancelled."
        )

    else:

        print(
            RED
            + "\n❌ Invalid choice."
            + RESET
        )


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        clear_screen()

        header()

        print("\n1. ➕ Add Website")
        print("2. ➖ Remove Website")
        print("3. 🔍 Check Single Website")
        print("4. 🌐 Check All Websites")
        print("5. 📊 Generate Report")
        print("6. 🔄 Continuous Monitoring")
        print("7. 🚪 Exit")

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":

            add_website()
            pause()

        elif choice == "2":

            remove_website()
            pause()

        elif choice == "3":

            check_single()
            pause()

        elif choice == "4":

            check_all()
            pause()

        elif choice == "5":

            generate_report()
            pause()

        elif choice == "6":

            continuous_monitor()
            pause()

        elif choice == "7":

            print(
                GREEN
                + "\nThanks for using SiteWatch! 👋"
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