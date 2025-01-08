# Qooper Scraper

A Selenium-based web scraper for Qooper that handles authentication and API queries.

## Prerequisites

1. ### Chrome and ChromeDriver
Grab the Chrome installer and driver from [Chrome Labs Testing Page](https://googlechromelabs.github.io/chrome-for-testing/) or alternatively run:

   ```bash
   # Install ChromeDriver

   wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/linux64/chromedriver-linux64.zip

   unzip chromedriver-linux64.zip

   sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
```

   > For WSL2 users, follow the additional Chrome setup instructions here: https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/

2. ### Environment Variables
Copy `.env.example` to `.env`
Fill in your credentials and required variables

```bash
cp .env.example .env
nano .env  # Or use your preferred editor
```

3. ### Running the Scraper

#### A. Install dependencies:
```bash
pip install -r requirements.txt
```
Ensure your .env file is configured

#### B. Run the scraper:
```bash
python scraper.py
```

## How it Works
- Uses Selenium to handle the complex sign-in process that involves multiple APIs and services
- Retrieves authentication tokens to query the Qooper API
- Automates data collection that would be difficult with traditional web scraping
