# Wildfire Dataset Processor
- Small utilities to inspect and reduce a large wildfire CSV for downstream analysis.

## Files
- `main.py` - Reads `Wildfire_Dataset.csv` in chunks, samples ~10% per chunk, filters rows (continental US bounding box), parses datetimes, saves a reduced CSV and a weekly aggregated summary.
- `inspect_columns.py` - Prints column names from `Wildfire_Dataset.csv` (useful to confirm available columns before running `main.py`).
- `requirements.txt` - Python dependencies (currently `pandas`).

## Prerequisites
- Python 3.8+
- pip
- Place the source dataset at `Wildfire_Dataset.csv` in the repository root (or update `SOURCE_FILE` in `main.py`).

## Installation
Install dependencies:
```
python -m pip install -r requirements.txt
```

## Usage
1. Inspect columns (optional):
```
python inspect_columns.py
```
2. Run the reduction and weekly aggregation:
```
python main.py
```
This will produce:
- `Wildfire_Dataset_sampled.csv` — reduced sample (approx. 100–150MB)
- `Wildfire_Dataset_weekly.csv` — weekly aggregated summary

## Configuration
Edit top of `main.py` to change:
- `SOURCE_FILE` — input CSV path
- `OUTPUT_SAMPLE`, `OUTPUT_WEEKLY` — output file names
- `chunksize` — rows per chunk
- `keep_columns` — columns to load
- Sampling fraction and grouping logic (currently samples 10% of each chunk and groups by ISO week)

## Notes & Best Practices
- `main.py` uses chunked reading to limit memory usage. Adjust `chunksize` for available RAM.
- Datetime parsing uses `errors='coerce'`; rows with invalid datetimes are dropped.
- Verify column names with `inspect_columns.py` before running if the dataset schema differs.
- If the dataset is very large, run on a machine with sufficient disk space for outputs.

## Troubleshooting
- "MemoryError": lower `chunksize`.
- Missing columns: run `inspect_columns.py` and update `keep_columns` in `main.py`.
- Encoding issues: pass `encoding='utf-8'` (or appropriate encoding) to `pd.read_csv` in `main.py`.

## License
MIT
