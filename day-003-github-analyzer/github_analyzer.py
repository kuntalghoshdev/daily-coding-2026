import json
import urllib.request
import urllib.error
from datetime import datetime


# ============================================================
# GITHUB PROFILE ANALYZER
# ============================================================

APP_NAME = "GITHUB PROFILE ANALYZER"
VERSION = "1.0"

API_BASE = "https://api.github.com"

REPORT_FILE = "github_report.json"


# ============================================================
# COLORS
# ============================================================

RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"


# ============================================================
# UI
# ============================================================

def clear_screen():
    print("\033[2J\033[H", end="")


def print_header():
    print(CYAN + "=" * 60 + RESET)
    print(CYAN + "             GITHUB PROFILE ANALYZER" + RESET)
    print(WHITE + f"                       Version {VERSION}" + RESET)
    print(CYAN + "=" * 60 + RESET)


def pause():
    input("\nPress Enter to continue...")


# ============================================================
# API REQUEST
# ============================================================

def api_request(endpoint):

    url = API_BASE + endpoint

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
            "User-Agent": "GitHub-Profile-Analyzer"
        }
    )

    try:

        with urllib.request.urlopen(request, timeout=15) as response:

            data = response.read().decode("utf-8")

            return (
                json.loads(data),
                response.headers
            )

    except urllib.error.HTTPError as error:

        if error.code == 404:
            print(
                RED
                + "\n❌ GitHub user or resource not found."
                + RESET
            )

        elif error.code == 403:
            print(
                RED
                + "\n❌ GitHub API rate limit may have been reached."
                + RESET
            )

            print(
                YELLOW
                + "Try again later."
                + RESET
            )

        else:
            print(
                RED
                + f"\n❌ GitHub API error: HTTP {error.code}"
                + RESET
            )

        return None, None

    except urllib.error.URLError as error:

        print(
            RED
            + "\n❌ Network error."
            + RESET
        )

        print(f"Details: {error.reason}")

        return None, None

    except TimeoutError:

        print(
            RED
            + "\n❌ Request timed out."
            + RESET
        )

        return None, None

    except json.JSONDecodeError:

        print(
            RED
            + "\n❌ Invalid response received from GitHub."
            + RESET
        )

        return None, None


# ============================================================
# GET USER PROFILE
# ============================================================

def get_profile(username):

    data, headers = api_request(
        f"/users/{username}"
    )

    if data is None:
        return None

    return data


# ============================================================
# GET ALL PUBLIC REPOSITORIES
# ============================================================

def get_repositories(username):

    repositories = []
    page = 1

    while True:

        endpoint = (
            f"/users/{username}/repos"
            f"?per_page=100"
            f"&page={page}"
            f"&sort=updated"
        )

        data, headers = api_request(endpoint)

        if data is None:
            return repositories

        if not data:
            break

        repositories.extend(data)

        if len(data) < 100:
            break

        page += 1

    return repositories


# ============================================================
# ANALYZE REPOSITORIES
# ============================================================

def analyze_repositories(repositories):

    total_stars = 0
    total_forks = 0

    original_repos = 0
    forked_repos = 0

    language_count = {}

    top_repositories = []

    for repo in repositories:

        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)

        total_stars += stars
        total_forks += forks

        if repo.get("fork"):
            forked_repos += 1
        else:
            original_repos += 1

        language = repo.get("language")

        if language:

            language_count[language] = (
                language_count.get(language, 0) + 1
            )

        top_repositories.append({
            "name": repo.get("name"),
            "stars": stars,
            "forks": forks,
            "language": language or "Unknown",
            "description": repo.get("description"),
            "url": repo.get("html_url"),
            "updated_at": repo.get("updated_at")
        })

    top_repositories.sort(
        key=lambda repo: (
            repo["stars"],
            repo["forks"]
        ),
        reverse=True
    )

    return {
        "total_repositories": len(repositories),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "original_repositories": original_repos,
        "forked_repositories": forked_repos,
        "languages": language_count,
        "top_repositories": top_repositories[:5]
    }


# ============================================================
# DEVELOPER SCORE
# ============================================================

def calculate_score(profile, repo_analysis):

    score = 0

    repos = repo_analysis["total_repositories"]
    stars = repo_analysis["total_stars"]
    followers = profile.get("followers", 0)
    original = repo_analysis["original_repositories"]

    # Repository points
    score += min(repos * 2, 30)

    # Original project points
    score += min(original * 2, 20)

    # Star points
    score += min(stars * 2, 20)

    # Followers
    score += min(followers, 20)

    # Following activity
    score += min(
        profile.get("following", 0) // 2,
        10
    )

    return min(score, 100)


# ============================================================
# SCORE MESSAGE
# ============================================================

def get_score_message(score):

    if score >= 90:
        return (
            "🔥 Exceptional developer profile!",
            "EXCEPTIONAL"
        )

    elif score >= 75:
        return (
            "🚀 Strong developer profile!",
            "STRONG"
        )

    elif score >= 60:
        return (
            "👍 Good developer profile!",
            "GOOD"
        )

    elif score >= 40:
        return (
            "📈 Growing developer profile.",
            "GROWING"
        )

    else:
        return (
            "🌱 Keep building and contributing!",
            "BEGINNER"
        )


# ============================================================
# DISPLAY PROFILE
# ============================================================

def display_profile(profile):

    print("\n" + BLUE + "👤 PROFILE" + RESET)
    print("-" * 60)

    print(
        f"Name             : "
        f"{profile.get('name') or 'Not provided'}"
    )

    print(
        f"Username         : "
        f"{profile.get('login')}"
    )

    print(
        f"Location         : "
        f"{profile.get('location') or 'Not provided'}"
    )

    print(
        f"Bio              : "
        f"{profile.get('bio') or 'Not provided'}"
    )

    print(
        f"Public Repos     : "
        f"{profile.get('public_repos', 0)}"
    )

    print(
        f"Followers        : "
        f"{profile.get('followers', 0)}"
    )

    print(
        f"Following        : "
        f"{profile.get('following', 0)}"
    )

    print(
        f"Profile          : "
        f"{profile.get('html_url')}"
    )


# ============================================================
# DISPLAY REPOSITORY ANALYSIS
# ============================================================

def display_repository_analysis(analysis):

    print("\n" + MAGENTA + "📊 REPOSITORY ANALYSIS" + RESET)
    print("-" * 60)

    print(
        f"Total Repositories : "
        f"{analysis['total_repositories']}"
    )

    print(
        f"Total Stars        : "
        f"{analysis['total_stars']}"
    )

    print(
        f"Total Forks        : "
        f"{analysis['total_forks']}"
    )

    print(
        f"Original Repos     : "
        f"{analysis['original_repositories']}"
    )

    print(
        f"Forked Repos       : "
        f"{analysis['forked_repositories']}"
    )


# ============================================================
# DISPLAY LANGUAGES
# ============================================================

def display_languages(analysis):

    print("\n" + CYAN + "💻 LANGUAGES" + RESET)
    print("-" * 60)

    languages = analysis["languages"]

    if not languages:

        print("No language information available.")

        return

    sorted_languages = sorted(
        languages.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for language, count in sorted_languages:

        print(
            f"{language:<20} : "
            f"{count} repositories"
        )


# ============================================================
# DISPLAY TOP REPOSITORIES
# ============================================================

def display_top_repositories(analysis):

    print(
        "\n"
        + YELLOW
        + "🏆 TOP REPOSITORIES"
        + RESET
    )

    print("-" * 60)

    repositories = analysis["top_repositories"]

    if not repositories:

        print("No repositories found.")

        return

    for index, repo in enumerate(
        repositories,
        start=1
    ):

        print(
            f"{index}. {repo['name']}"
        )

        print(
            f"   ⭐ {repo['stars']}  "
            f"🍴 {repo['forks']}  "
            f"💻 {repo['language']}"
        )

        if repo["description"]:

            print(
                f"   {repo['description']}"
            )

        print(
            f"   {repo['url']}"
        )

        print()


# ============================================================
# DISPLAY SCORE
# ============================================================

def display_score(score):

    message, level = get_score_message(score)

    print(
        "\n"
        + GREEN
        + "🔥 DEVELOPER SCORE"
        + RESET
    )

    print("-" * 60)

    print(
        f"Score: {score}/100"
    )

    print(
        f"Level: {level}"
    )

    print(message)


# ============================================================
# EXPORT REPORT
# ============================================================

def export_report(
    profile,
    analysis,
    score
):

    report = {
        "generated_at": datetime.now().isoformat(),

        "profile": {
            "name": profile.get("name"),
            "username": profile.get("login"),
            "location": profile.get("location"),
            "bio": profile.get("bio"),
            "public_repositories": profile.get(
                "public_repos",
                0
            ),
            "followers": profile.get(
                "followers",
                0
            ),
            "following": profile.get(
                "following",
                0
            ),
            "profile_url": profile.get(
                "html_url"
            )
        },

        "repository_analysis": analysis,

        "developer_score": score
    }

    try:

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
            + f"\n✅ Report exported to {REPORT_FILE}"
            + RESET
        )

    except OSError as error:

        print(
            RED
            + "\n❌ Could not export report."
            + RESET
        )

        print(error)


# ============================================================
# ANALYZE USER
# ============================================================

def analyze_user():

    username = input(
        "\nEnter GitHub username: "
    ).strip()

    if not username:

        print(
            RED
            + "\n❌ Username cannot be empty."
            + RESET
        )

        return

    print(
        "\n"
        + YELLOW
        + "Fetching GitHub profile..."
        + RESET
    )

    profile = get_profile(username)

    if profile is None:
        return

    print(
        GREEN
        + "✓ Profile loaded"
        + RESET
    )

    print(
        YELLOW
        + "Fetching repositories..."
        + RESET
    )

    repositories = get_repositories(username)

    print(
        GREEN
        + f"✓ {len(repositories)} repositories loaded"
        + RESET
    )

    analysis = analyze_repositories(
        repositories
    )

    score = calculate_score(
        profile,
        analysis
    )

    clear_screen()
    print_header()

    display_profile(profile)

    display_repository_analysis(
        analysis
    )

    display_languages(
        analysis
    )

    display_top_repositories(
        analysis
    )

    display_score(score)

    export_choice = input(
        "\nExport report to JSON? (y/n): "
    ).strip().lower()

    if export_choice == "y":

        export_report(
            profile,
            analysis,
            score
        )


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        clear_screen()
        print_header()

        print("\n1. 🔍 Analyze GitHub Profile")
        print("2. 🚪 Exit")

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":

            analyze_user()

            pause()

        elif choice == "2":

            print(
                GREEN
                + "\nThanks for using GitHub Profile Analyzer! 👋"
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
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()