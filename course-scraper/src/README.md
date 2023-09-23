# Getting Started

0. Google Skill Boost Login
   Setup your email address and password, OAuth login with Google won't work with this script.
   You might also need to download a different chromedriver binary version. The version in this repo works with Chrome 117

1. Setup and activate your Virtual environment
   Create a new virtual environment.

```
    python -m venv venv
```

Activate it (Windows)

```
./venv/scripts/activate
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Run the scripts

- Scrape a Journey: (Should always be run first for each journey)
  (e.g https://www.cloudskillsboost.google/journeys/183)

```
python -m scrapers.scrape_journey
```

- Scrape a Course Template:
  > (e.g https://www.cloudskillsboost.google/course_templates/541

```
python -m scrapers.scrape_course_template
```

- TODO: Scrape a Lab/Focus:
  > (e.g https://www.cloudskillsboost.google/focuses/71938?parent=catalog)

```
python -m scrapers.scrape_focus
```

## Config
Most of the behaviour and parameters of scraping can be modified from `config.py`

JOURNEY_URL = "URL on Google Cloud boost"
JOURNEY_CODE = "Course Code on the Learning Index"

# TODO

- Maybe switch from using Selenium to regular requests. Most courses and their information are publicly accessible

## Notes for Nerds

### Selenium necessary?

### Why use Pydantic?

Pretty lazy about the JSON parsing. With pydantic models, I could use dot access which feels faster and cleaner to me. Sometimes you want to write the fastest code, other times you want to write code the fastest :)
