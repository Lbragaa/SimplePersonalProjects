- HoYoLAB Daily Check-In Automation

This project automates the daily check-in process for HoYoLAB (Genshin Impact and Honkai Star Rail). It securely logs into the official HoYoLAB API, performs daily sign-ins, and sends a notification with the result to a Discord channel.

The automation runs on GitHub Actions, allowing it to work daily in the cloud without needing to keep your PC on.

Features
Automated daily check-ins for: Genshin Impact, Honkai Star Rail, Zenless Zone Zero
Discord webhook notifications with the check-in results
Secure authentication using GitHub Secrets
Runs automatically every day at 20:00 (Brasília time) via GitHub Actions
DS signature generation for secure API requests
Technologies Used
Python (requests, hashlib)
GitHub Actions (CI/CD)
REST APIs and HTTP requests
JSON handling
Discord Webhooks
Git and GitHub for version control

Disclaimer: This project interacts only with official HoYoLAB APIs, respecting game terms of service. It does not automate gameplay or bypass anti-cheat mechanisms.