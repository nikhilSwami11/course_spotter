# Deployment Guide: GitHub Actions (Free)

This guide shows you how to run this monitoring script for free using **GitHub Actions**. It will check for seats every 10 minutes.

## Steps

1.  **Create a Repository on GitHub**
    - Go to GitHub and create a new **Public** or **Private** repository.

2.  **Upload Files**
    - Upload `monitor.py`, `requirements.txt`, and the `.github` folder to your repository.
    - *Note: Do NOT upload your `.env` file.*

3.  **Add Your Secret**
    - Go to your repository **Settings** > **Secrets and variables** > **Actions**.
    - Click **New repository secret**.
    - **Name**: `TELEGRAM_BOT_TOKEN`
    - **Value**: `8134275823:AAEBsHJ-Pr2tAimkXFPHckaikLDBWctLR0I` (Your token)
    - Click **Add secret**.

4.  **Activate**
    - Once the files are pushed and the secret is added, go to the **Actions** tab in your repository.
    - You should see the "ASU Course Monitor" workflow.
    - You can manually trigger it with "Run workflow" to test, or wait for the 10-minute schedule.

## Notes
- **Frequency**: The workflow triggers **every 6 minutes**.
- **Internal Loop**: Unlike a normal cron, the script stays alive and checks **every 2 minutes** (3 checks per run). This efficiently bypasses GitHub's 5-minute scheduler limit to give you faster notifications.
- **Cost**: Still free for public repositories.

