# Getting Started

This guide will help you set up and run the Learning Path Index (LPI) project on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python (tested with version 3.x):** Download and install Python from [the official website](https://www.python.org/downloads/).
- **Git:** Download and install Git from [the official website](https://git-scm.com/downloads).
- **Docker (optional):** While not strictly necessary, Docker simplifies running certain components. Install Docker following the [instructions for your operating system](https://docs.docker.com/get-docker/).

## Installation

The LPI project consists of several independent applications (applets) that work together:

- **Web scraper**
- **LLM Variant 01 (Ollama)**
- **LLM Variant 02 (OpenAI)**

**Note:** This guide focuses on setting up the general repository. Each applet may have additional instructions.

### Step 1: Clone the Repository

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/neomatrix369/learning-path-index.git learning-path-index

cd learning-path-index
```

### Step 2: Install Dependencies

Python dependencies for each applet are located in the `./requirements/` directory, with each applet having a separate file. Here's how to install them using a virtual environment:

#### Create a virtual environment:

```bash
python -m venv venv
```

#### Activate the virtual environment

MacOS/Linux

```bash
. venv/bin/activate
```

Windows

```powershell
venv\Scripts\activate
```

#### Install base dependencies

```bash
pip install -r requirements/base.txt
```

#### Install dependencies for specific applets

Each applet may have additional dependencies. Look for a requirements.txt file within the directory for the specific applet (e.g., requirements/scraper.txt) and install them using:

```bash
pip install -r requirements/<applet_name>.txt
```

Replace `<applet_name>` with the actual name of the applet (e.g., `scraper`).

### Step 3: Setup pre-commit hooks

Pre-commit hooks automate tasks like code formatting and linting. Install them using:

```bash
pre-commit install
```

### Step 4: Setup the Applets

Each applet has its own setup and usage instructions. Refer to the documentation specific to each applet for detailed guidance on:

- Web scraper: [Installation instructions and usage guide](app/course-scraper/README.md).

- LLM Variant 01 (Ollama): [Instructions on setting up and using Ollama](app/llm-poc-variant-01/deploy/aws/README.md).

- LLM Variant 02 (OpenAI): [Instructions on creating an OpenAI account and API keys](app/llm-poc-variant-02/README.md).

**Tip**: Look for additional documentation files within the directory for each applet.

## Troubleshooting

Here are some common issues or errors that you might face:

- Dependency Conflicts: Ensure that your dependencies are up to date and consistent with the versions specified in the requirements directory.
- OpenAI Rate limit error: The free tier of OpenAI has limitations on API calls. Consider upgrading to a paid account if you frequently encounter this error.

For further assistance, refer to the project's documentation (if available) or reach out to the project maintainers on the GitHub repository.
