# Lidl Receipt Analyzer

A Python tool to extract and analyze your personal Lidl Plus receipt history using the Lidl web API.

## What it does

- Extracts all your Lidl receipts via the Lidl Plus API
- Parses item-level data (name, quantity, unit price, total) from receipt HTML
- Produces a clean JSON dataset ready for analysis
- Jupyter notebook with spending trends, price inflation tracking, and item loyalty scores

## Prerequisites

- Python 3.9+
- Google Chrome with [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) extension
- A Lidl Plus account with purchase history

## Installation
```bash
git clone https://github.com/YOUR_USERNAME/lidl-analyzer.git
cd lidl-analyzer
pip install -r requirements.txt
```

## Usage

### Step 1 — Export your session cookies

1. Log into [lidl.de/mla/purchases](https://www.lidl.de/mla/purchases) in Chrome
2. Click Cookie-Editor → Export → copy to clipboard
3. Save as `lidl_cookies.json` in the project folder
4. Open Chrome DevTools → Network → click the `tickets?country=DE` request → copy the `x-xsrf-token` header value

### Step 2 — Update session
```bash
python3 update_cookies.py
```
Paste the XSRF-TOKEN when prompted. This creates `session.json`.

### Step 3 — Extract receipts
```bash
python3 extract_all.py
```
Downloads all your receipts to `lidl_receipts.json`.

### Step 4 — Build clean dataset
```bash
python3 build_dataset.py
```
Parses item-level data into `lidl_clean.json`.

### Step 5 — Analyse
```bash
jupyter notebook analysis.ipynb
```

## Output

| File | Description |
|------|-------------|
| `lidl_receipts.json` | Raw receipt data from API |
| `lidl_clean.json` | Parsed item-level dataset |

> ⚠️ Both files contain personal data and are excluded from git via `.gitignore`

## Security notice

- Never commit `session.json`, `lidl_cookies.json`, `lidl_receipts.json` or `lidl_clean.json`
- Session cookies expire after ~1 hour — re-run `update_cookies.py` if you get 401 errors
- All data stays local on your machine

## License

MIT
