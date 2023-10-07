# Kaggle Learn Course Scraper

This folder contains scripts for scraping courses from the Kaggle Learn website using the Kaggle Learn API. The scripts retrieve course information in JSON format without the need for HTML parsing.

## Scripts

1. **`scrape_all_courses.py`**: This script makes use of the Kaggle Learn API to scrape all available courses from the platform in a single API request. It's the recommended script to use when scraping a comprehensive list of courses.

2. **`scrape_course.py`**: This script is provided for illustrative purposes. It demonstrates how to scrape course information using the Kaggle Learn API on a per-course basis.

## Getting Started

To get started with course scraping, you can choose between the two scripts mentioned above based on your requirements.

### Prerequisites

Make sure you have Python installed on your system.

### Usage

1. Clone this repository

2. Navigate to the repository folder:

```bash
cd course-scraper/src
```

3. Run the desired script:

```bash
python -m scrapers.kaggle_learn.scrape_all_courses
```

or

```bash
python -m scrapers.kaggle_learn.scrape_all_course
```

## Config

The folder where the output is stored can be changed by modifying `course-scraper/config.py`