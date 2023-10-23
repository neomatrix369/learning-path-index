# Course Scraper Module

The Course Scraper Module is a versatile tool designed to fetch course information and duration from various online learning platforms. It simplifies the process of extracting course metadata and information from a range of sources using web scraping.

## Supported Platforms

- [x] Google Developer Courses
- [x] Fast.ai ML Course
- [x] IBM - AI & Ethics Course
- [ ] Google Cloud Skill Boost: Machine Learning Engineer
- [x] Google Cloud Skill Boost: Data Learning Engineer
- [ ] Google Cloud Skill Boost: Data Analyst
- [x] Google Cloud Skill Boost: Generative AI
- [ ] Google Cloud Skill Boost: AD-HOC Courses
- [ ] [Kaggle Learn Courses](./src/scrapers/kaggle_learn)
- [ ] Deeplearning.ai Courses

## Getting Started

To get started with the Course Scraper Module, follow these steps:

1. **Clone the Repository:**

   Clone this GitHub repository to your local machine:


2. **Navigate to the Course Scraper Module:**

   Change your current working directory to the course-scraper subfolder within the cloned repository:

   ```bash
   cd learning-path-index/course-scraper
   ```

3. **Install Dependencies:**

   Ensure you have all the required dependencies installed. You can do this using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Scraper:**

   Scrapers specific to each platform can be found in `course-scraper/src/scrapers` folder.
   Would you like to scrape courses from *Kaggle Learn*?
   Checkout the [Kaggle Learn scraper README.md]().
   How about *Google Cloud Skill Boost*?
   Checkout the [GCSB scraper README.md]().
   

   Generally scrapers can be run by navigating to the `course-scraper/src` folder, and running
   ```bash
   python -m scrapers.<course_platform>.<specific_script>
   ```

   e.g

   ```bash
   python -m scrapers.kaggle_learn.scrape_all_courses
   ```


5. **View the Results:**

   The scraper will provide the course details and duration in a structured format. In the folder determined by `config.py`

## Usage

### Scraper Configuration

You can configure the general behaviour of all scrapers by modifying the `config.py` file. This file allows you to specify:
 -  output location ✅
 -  the output format (TODO: 🚧), 

and other settings.

## Contributing

We welcome contributions to enhance and expand the Course Scraper Module. If you'd like to contribute, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and ensure that the code passes all tests.
4. Submit a pull request with a clear description of your changes and their purpose.


Happy learning and scraping!