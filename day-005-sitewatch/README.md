# 🌐 SiteWatch

A Python CLI website uptime monitoring tool that checks website availability, HTTP status, and response time.

## ✨ Features

- Check a single website
- Monitor multiple websites
- Measure response time
- Detect offline websites
- Detect timeouts
- Detect slow websites
- Display HTTP status codes
- Add websites
- Remove websites
- Continuous monitoring
- JSON reports
- CSV reports
- Average response time
- Colored CLI interface
- No external Python packages required

## 📊 Status

| Status | Meaning |
|---|---|
| 🟢 ONLINE | Response under 500 ms |
| 🟡 SLOW | Response between 500–1500 ms |
| 🟠 VERY SLOW | Response above 1500 ms |
| 🔴 OFFLINE | Connection failed |
| ⏱️ TIMEOUT | Server didn't respond in time |

## 🛠️ Technology

- Python 3
- urllib
- JSON
- CSV
- datetime
- time

## ▶️ Run

```bash
python sitewatch.py

📋 Example
=============================================================
                    🌐 SITEWATCH
                 Website Uptime Monitor
=============================================================


Website                             Status          Response
----------------------------------------------------------------------
https://google.com                  🟢 ONLINE       180 ms
https://github.com                  🟢 ONLINE       240 ms
https://example.com                 🟢 ONLINE       310 ms
----------------------------------------------------------------------


Checked : 3 websites
Online  : 3
Slow    : 0
Offline : 0


Average response time: 243.33 ms
📄 Reports

The application can generate:

uptime_report.json
uptime_report.csv

These generated reports are ignored by Git.