# Trading Portfolio Risk Analysis

## Overview
This repository analyzes a stock portfolio from a CSV file, calculates risk metrics (beta and weekly implied volatility proxy), and generates visual outputs. It also includes an automation script that runs the analysis and emails the results.

## Key Files
- [stock_portfolio_risk.py](stock_portfolio_risk.py) — main script that loads positions, fetches market data, and generates analysis outputs.
- [import_subprocess.py](import_subprocess.py) — automation runner that executes the analysis and emails results.
- [Analyze_risk.ipynb](Analyze_risk.ipynb) — notebook version of the analysis workflow.
- [Positions_main.csv](Positions_main.csv) — input portfolio file (tickers + shares/position).

## Outputs
The analysis script writes output files in the workspace root:
- portfolio_analysis.csv
- portfolio_analysis.png
- portfolio_iv_history.html
- portfolio_iv_history.png

These outputs are ignored by git by default.

## Setup
1. Create and activate a virtual environment.
2. Install dependencies from [requirements.txt](requirements.txt).
3. Set email environment variables for automation:
   - TRADING_EMAIL_TO
   - TRADING_EMAIL_FROM
   - TRADING_EMAIL_PASSWORD

An example file is provided at [.env.example](.env.example).

## Usage
- Run the analysis:
  - python stock_portfolio_risk.py
- Run the automation runner (emails results):
  - python import_subprocess.py

## Notes
- The automation script uses the current Python interpreter (sys.executable).
- Gmail requires an App Password for SMTP.
- The CSV must include ticker and shares columns (common variants like Ticker/Shares are supported).
