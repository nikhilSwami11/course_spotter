# ASU Course Spotter

A Python bot that monitors seat availability for specific Arizona State University (ASU) graduate courses and sends real-time Telegram notifications.

## 🎯 Target Courses
This bot is currently configured to watch the following **Tempe Campus** classes (Spring 2026):
- **CSE 572**: Data Mining (Class #22907)
- **CSE 573**: Semantic Web Mining (Class #37582)
- **CSE 578**: Data Visualization (Class #27108)

## 🚀 How it Works
The script checks the ASU Course Catalog API every **2 minutes**. If a seat opens up (Enrollment < Capacity), it immediately sends a message to your Telegram.

### 雲 Cloud Deployment (GitHub Actions)
This project is set up to run **automatically and for free** using GitHub Actions.
- The workflow (`.github/workflows/monitor.yml`) triggers every 6 minutes.
- It runs an internal loop to check every 2 minutes, ensuring continuous coverage.

## 🛠️ Setup
1. **Fork/Clone** this repository.
2. **Add Secret**: Go to `Settings` > `Secrets and variables` > `Actions`.
   - Add a repository secret named `TELEGRAM_BOT_TOKEN` with your bot token.
3. **Done!** The monitoring will start automatically.

## 💻 Local Usage
To run locally:
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file with your token:
   ```text
   TELEGRAM_BOT_TOKEN=your_token_here
   ```
3. Run the script:
   ```bash
   python monitor.py
   ```
