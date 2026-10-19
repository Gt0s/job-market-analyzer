"""Analyze a CSV of job postings and summarize common technical skills."""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DEFAULT_INPUT = Path(__file__).parent / "data" / "sample_jobs.csv"
OUTPUT_DIR = Path(__file__).parent / "output"

# A simple keyword list. This is intentionally transparent and easy to customize.
SKILLS = [
    "python", "java", "javascript", "sql", "pandas", "machine learning",
    "spring boot", "rest api", "git", "docker", "linux", "networking",
    "tcp/ip", "dns", "cybersecurity", "excel", "data visualization",
    "statistics", "troubleshooting", "windows",
]


def load_jobs(path: Path) -> pd.DataFrame:
    """Load and validate a job-postings CSV."""
    if not path.exists():
        raise FileNotFoundError(f"Input CSV not found: {path}")

    jobs = pd.read_csv(path).fillna("")
    required = {"title", "description"}
    missing = required - set(jobs.columns)
    if missing:
        raise ValueError(
            "CSV is missing required column(s): " + ", ".join(sorted(missing))
        )
    if jobs.empty:
        raise ValueError("The input CSV contains no job postings.")
    return jobs


def count_skills(jobs: pd.DataFrame) -> pd.DataFrame:
    """Count postings that mention each skill at least once."""
    text = (jobs["title"].astype(str) + " " + jobs["description"].astype(str)).str.lower()
    rows = []
    for skill in SKILLS:
        # Count postings containing the skill, not every repeated mention.
        count = int(text.str.contains(skill.lower(), regex=False).sum())
        if count:
            rows.append({"skill": skill, "job_postings": count})

    result = pd.DataFrame(rows, columns=["skill", "job_postings"])
    if not result.empty:
        result = result.sort_values(
            ["job_postings", "skill"], ascending=[False, True]
        ).reset_index(drop=True)
    return result


def save_outputs(results: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / "skill_frequency.csv"
    chart_path = OUTPUT_DIR / "skill_frequency.png"
    results.to_csv(csv_path, index=False)

    if results.empty:
        print("No matching skills were found; saved an empty CSV.")
        return

    chart_data = results.head(12).sort_values("job_postings")
    plt.figure(figsize=(10, 6))
    plt.barh(chart_data["skill"], chart_data["job_postings"])
    plt.xlabel("Number of job postings mentioning skill")
    plt.ylabel("Skill")
    plt.title("Most frequently requested skills in the supplied dataset")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=160)
    plt.close()

    print(f"Analyzed skills in {len(results)} skill categories.")
    print("\nTop skills:")
    print(results.head(10).to_string(index=False))
    print(f"\nCSV report: {csv_path}")
    print(f"Chart:      {chart_path}")


def main() -> int:
    input_path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_INPUT
    try:
        jobs = load_jobs(input_path)
        results = count_skills(jobs)
        print(f"Loaded {len(jobs)} job postings from: {input_path}")
        save_outputs(results)
    except (OSError, ValueError, pd.errors.ParserError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
