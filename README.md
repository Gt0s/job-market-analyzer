# Job Market Analyzer

A small Python project that analyzes job-posting data stored in a CSV file and summarizes which technical skills appear most often.

## Features
- Reads job postings from `data/sample_jobs.csv`
- Counts skill mentions from job titles and descriptions
- Saves the results to `output/skill_frequency.csv`
- Creates a chart at `output/skill_frequency.png`
- Prints a short summary to the terminal

## Requirements
- Python 3.10 or newer

## Run in VS Code
Open this folder in VS Code, then run these commands in the terminal:

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install packages and run:
```bash
python -m pip install -r requirements.txt
python analyze_jobs.py
```

You can optionally pass another CSV file:
```bash
python analyze_jobs.py path/to/jobs.csv
```

The CSV must contain `title` and `description` columns. `company` and `location` are optional.

## Example data
The included data is synthetic sample data for demonstration, not a real-time labor-market survey. Results depend on the data you provide.

## Ideas to extend it
- Add skills relevant to Greek job ads
- Compare skills by location or job title
- Add a command-line option for the number of skills shown
- Add tests for skill extraction
- Export a short Markdown report

## Portfolio note
Before publishing, add a section describing your own changes and the limitations of keyword-based skill detection.
