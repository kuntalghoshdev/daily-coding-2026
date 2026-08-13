# 🔍 GitHub Profile Analyzer

A Python CLI application that analyzes public GitHub profiles using the GitHub REST API.

## ✨ Features

- Analyze any public GitHub user
- Fetch public profile information
- Count public repositories
- Count total stars
- Count total forks
- Separate original and forked repositories
- Analyze repository languages
- Display top repositories
- Calculate a developer score
- Export the complete analysis as JSON
- Handle GitHub API errors
- Handle network errors
- Handle invalid usernames

## 📊 Analysis

The application analyzes:

- Public repositories
- Followers
- Following
- Repository stars
- Repository forks
- Repository languages
- Original vs forked repositories
- Top repositories

## 🧮 Developer Score

The application calculates a simple profile score based on:

- Repository count
- Original projects
- Stars
- Followers
- Following activity

The score is intended for experimentation and is not an official GitHub metric.

## 📄 JSON Export

The application can export the analysis to:

```text
github_report.json

🛠️ Technologies
Python 3
GitHub REST API
urllib
JSON
pathlib-style file handling
CLI

▶️ Run
python github_analyzer.py


💻 Example
============================================================
             GITHUB PROFILE ANALYZER
                       Version 1.0
============================================================

1. 🔍 Analyze GitHub Profile
2. 🚪 Exit

Choose an option: 1

Enter GitHub username: kuntalghoshdev

Fetching GitHub profile...
✓ Profile loaded
Fetching repositories...
✓ repositories loaded

👤 PROFILE
------------------------------------------------------------
Name             : Kuntal Ghosh
Username         : kuntalghoshdev
Location         : India
Public Repos     : ...
Followers        : ...
Following        : ...

📊 REPOSITORY ANALYSIS
------------------------------------------------------------
Total Repositories : ...
Total Stars        : ...
Total Forks        : ...
Original Repos     : ...
Forked Repos       : ...

🔥 DEVELOPER SCORE
------------------------------------------------------------
Score: .../100