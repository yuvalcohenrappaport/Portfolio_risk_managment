import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime, timedelta

plt.style.use('dark_background')

TICKERS = ['AMZN','GOOG','ONDS','RCL','VUG','TSM','IREN','LPTH','CCJ','SMR','V','FORM','ANF','AMD','BTU','SGMO','BMNR']
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'company_reports')
os.makedirs(OUTPUT_DIR, exist_ok=True)

results = {}

for ticker in TICKERS:
    print(f"\n--- {ticker} ---")
    try:
        stock = yf.Ticker(ticker)

        # Fetch 12 months of price history
        hist = stock.history(period="1y")
        if hist.empty:
            print(f"  No price data for {ticker}")
            results[ticker] = {"error": "No price data"}
            continue

        # Save price history CSV
        hist.to_csv(os.path.join(OUTPUT_DIR, f"{ticker}_price_history.csv"))

        # Get info for P/B ratio
        info = stock.info
        pb_ratio = info.get('priceToBook', None)
        company_name = info.get('longName', info.get('shortName', ticker))
        sector = info.get('sector', 'N/A')
        industry = info.get('industry', 'N/A')
        market_cap = info.get('marketCap', None)
        pe_ratio = info.get('trailingPE', None)
        forward_pe = info.get('forwardPE', None)
        dividend_yield = info.get('dividendYield', None)
        book_value = info.get('bookValue', None)

        print(f"  Company: {company_name}")
        print(f"  Sector: {sector}")
        print(f"  P/B Ratio: {pb_ratio}")
        print(f"  Book Value: {book_value}")

        # Try to get quarterly P/B history using quarterly balance sheet + price
        quarterly_pb = []
        try:
            bs = stock.quarterly_balance_sheet
            if bs is not None and not bs.empty:
                # Get total stockholders equity and shares outstanding
                for date_col in bs.columns:
                    equity = None
                    for key in ['Stockholders Equity', 'Total Stockholder Equity', 'Stockholder Equity',
                                'Common Stock Equity', 'Ordinary Shares Number']:
                        if key in bs.index:
                            equity = bs.loc[key, date_col]
                            break

                    shares = None
                    for key in ['Share Issued', 'Shares Outstanding', 'Ordinary Shares Number']:
                        if key in bs.index:
                            shares = bs.loc[key, date_col]
                            break

                    if equity is not None and shares is not None and shares > 0:
                        bv_per_share = equity / shares
                        # Get price closest to that date
                        target_date = pd.Timestamp(date_col)
                        if target_date.tzinfo is not None:
                            target_date = target_date.tz_localize(None)

                        hist_no_tz = hist.copy()
                        hist_no_tz.index = hist_no_tz.index.tz_localize(None)

                        # Find nearest price
                        idx = hist_no_tz.index.get_indexer([target_date], method='nearest')[0]
                        if 0 <= idx < len(hist_no_tz):
                            price_at_date = hist_no_tz.iloc[idx]['Close']
                            pb_at_date = price_at_date / bv_per_share if bv_per_share > 0 else None
                            if pb_at_date is not None:
                                quarterly_pb.append({
                                    'date': str(target_date.date()),
                                    'pb_ratio': float(pb_at_date),
                                    'book_value': float(bv_per_share),
                                    'price': float(price_at_date)
                                })
        except Exception as e:
            print(f"  Could not compute quarterly P/B: {e}")

        # Sort quarterly P/B by date
        quarterly_pb.sort(key=lambda x: x['date'])

        # Generate price chart
        fig, axes = plt.subplots(1, 2, figsize=(16, 5))

        # Price chart
        ax1 = axes[0]
        ax1.plot(hist.index, hist['Close'], color='#00d4ff', linewidth=1.5)
        ax1.fill_between(hist.index, hist['Close'], alpha=0.15, color='#00d4ff')
        ax1.set_title(f'{ticker} - 12 Month Price', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Price ($)')
        ax1.grid(alpha=0.3)

        # P/B chart
        ax2 = axes[1]
        if quarterly_pb:
            dates = [pd.Timestamp(x['date']) for x in quarterly_pb]
            pbs = [x['pb_ratio'] for x in quarterly_pb]
            ax2.bar(dates, pbs, width=25, color='#ff6b6b', alpha=0.8, edgecolor='white', linewidth=0.5)
            ax2.axhline(y=pb_ratio if pb_ratio else pbs[-1], color='yellow', linestyle='--', alpha=0.7, label=f'Current: {pb_ratio:.2f}' if pb_ratio else '')
            ax2.legend()
            ax2.set_title(f'{ticker} - P/B Ratio (Quarterly)', fontsize=14, fontweight='bold')
            ax2.set_ylabel('P/B Ratio')
            ax2.grid(alpha=0.3)
        elif pb_ratio is not None:
            ax2.bar([ticker], [pb_ratio], color='#ff6b6b', alpha=0.8)
            ax2.set_title(f'{ticker} - Current P/B: {pb_ratio:.2f}', fontsize=14, fontweight='bold')
            ax2.set_ylabel('P/B Ratio')
            ax2.grid(alpha=0.3)
        else:
            ax2.text(0.5, 0.5, 'P/B Data\nNot Available', ha='center', va='center', fontsize=16, color='gray', transform=ax2.transAxes)
            ax2.set_title(f'{ticker} - P/B Ratio', fontsize=14, fontweight='bold')

        plt.tight_layout()
        chart_path = os.path.join(OUTPUT_DIR, f"{ticker}_charts.png")
        plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='#1a1a1a')
        plt.close()
        print(f"  Charts saved: {chart_path}")

        results[ticker] = {
            "company_name": company_name,
            "sector": sector,
            "industry": industry,
            "market_cap": market_cap,
            "pb_ratio": pb_ratio,
            "pe_ratio": pe_ratio,
            "forward_pe": forward_pe,
            "dividend_yield": dividend_yield,
            "book_value": book_value,
            "quarterly_pb": quarterly_pb,
            "chart_path": chart_path,
            "current_price": float(hist['Close'].iloc[-1]),
            "price_52w_high": float(hist['Close'].max()),
            "price_52w_low": float(hist['Close'].min()),
            "price_change_12m": float((hist['Close'].iloc[-1] / hist['Close'].iloc[0] - 1) * 100)
        }

    except Exception as e:
        print(f"  ERROR: {e}")
        results[ticker] = {"error": str(e)}

# Save all results as JSON
with open(os.path.join(OUTPUT_DIR, 'all_data.json'), 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"\n\nAll data saved to {OUTPUT_DIR}/all_data.json")
print(f"Charts saved for {sum(1 for v in results.values() if 'error' not in v)} tickers")
