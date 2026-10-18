# Python Automation Engineering Lab

A Python automation project that retrieves repository data from the GitHub API, processes repository activity, and generates structured JSON reports.

The project demonstrates practical software engineering skills, including API authentication, pagination, error handling, automatic retries, exponential backoff, logging, data transformation, and automated testing with pytest.

## Features

- **GitHub API integration:** Retrieves repository information using authenticated API requests.
- **Pagination:** Fetches repositories across multiple API response pages.
- **Repository activity analysis:** Classifies repositories as Active or Stale based on their last push date.
- **Data processing:** Extracts relevant repository details and calculates summary statistics.
- **JSON reporting:** Saves structured repository data and summary information to a JSON file.
- **Error handling and retries:** Handles network failures and retries temporary errors using exponential backoff.
- **Logging:** Records application activity, errors, and API rate-limit information.
- **Automated testing:** Uses pytest and mocking to verify data processing, API behavior, and retry logic.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/irfan5511/python-automation-engineering-lab.git
```

### 2. Navigate to the project directory

```bash
cd python-automation-engineering-lab
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
```

### 4. Activate the virtual environment

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

Install the packages required to run the application:

```bash
python -m pip install -r requirements.txt
```

For development and automated testing, install the additional dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

## Configuration

The application requires a GitHub personal access token to access authenticated GitHub API endpoints.

### 1. Create an environment file

Copy the example environment file:

**macOS / Linux:**

```bash
cp .env.example .env
```

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

### 2. Configure the GitHub token

Open the `.env` file and set your GitHub personal access token:

```dotenv
GITHUB_TOKEN=your_github_personal_access_token
```

Generate your own personal access token from GitHub's developer settings. Use only the permissions required by the application.

Never commit `.env` or share your actual token publicly.

## Usage

After installing the dependencies and configuring your GitHub token, run the application:

```bash
python main.py
```

The application retrieves repositories from the authenticated GitHub account, processes repository activity, and generates a JSON report at:

```text
data/github_irfan_repositories.json
```

## Testing

The project uses **pytest** for automated testing.

Install the development dependencies if you haven't already:

```bash
python -m pip install -r requirements-dev.txt
```

Run the complete test suite:

```bash
python -m pytest
```

The tests cover repository data processing, activity classification, JSON reporting, mocked GitHub API responses, HTTP error handling, retries, and exponential backoff.