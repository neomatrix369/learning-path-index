# Getting Started

1. **Setup Your Virtual Environment**
   - Create a new virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate

   #Windows
   venv/Scripts/activate
   ```

2. **Install Dependencies**

- Change to the appropriate directory

   ```bash
   cd C:/{path}/learning-path-index/app/course-scraper
   ```


- Run the following command to install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Scripts**

   - **Scrape a Journey** (Run this first for each journey)
     - Example:
     To scrape the ML Engineer Path (https://www.cloudskillsboost.google/journeys/183)
     modify the config variables in `scrape_journey.py` and run
     ```bash
     python -m scrapers.google_cloud_skill_boost.scrape_journey
     ```

   - **Scrape a Course Template**
     - Example:
    To scrape the details of all the courses in the ML Engineer Path (Details of Learning Paths are termed course templates e.g https://www.cloudskillsboost.google/course_templates/541),
     ```bash
     python -m scrapers.scrapers.google_cloud_skill_boost.scrape_course_template
     ```

   - **TODO: Scrape a Lab/Focus**
     - Example:
    To scrape the details of a lab (An example lab is https://www.cloudskillsboost.google/focuses/71938?parent=catalog)
     ```bash
     python -m scrapers.scrapers.google_cloud_skill_boost.scrape_focus
     ```

## Configuration
You can modify most of the scraping behavior and parameters by editing the `config.py` file.
