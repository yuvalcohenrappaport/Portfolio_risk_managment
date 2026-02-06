import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Apply dark mode
plt.style.use('dark_background')

def get_weekly_iv(stock, current_price):
    """Calculate weekly IV by dividing yearly IV by 7."""
    try:
        expirations = stock.options
        if not expirations:
            return np.nan

        # Get the nearest expiration for IV data
        chain = stock.option_chain(expirations[0])

        if chain.calls.empty and chain.puts.empty:
            return np.nan

        # Find closest strike to current price
        calls = chain.calls.copy()
        puts = chain.puts.copy()

        if not calls.empty:
            calls['strike_diff'] = (calls['strike'] - current_price).abs()
            call_row = calls.loc[calls['strike_diff'].idxmin()]
            call_iv = call_row.get('impliedVolatility', np.nan)
        else:
            call_iv = np.nan

        if not puts.empty:
            puts['strike_diff'] = (puts['strike'] - current_price).abs()
            put_row = puts.loc[puts['strike_diff'].idxmin()]
            put_iv = put_row.get('impliedVolatility', np.nan)
        else:
            put_iv = np.nan

        yearly_iv = np.nanmean([call_iv, put_iv])
        # Convert yearly IV to weekly IV by dividing by 7
        weekly_iv = yearly_iv / 7
        return weekly_iv
    except Exception:
        return np.nan


def get_historical_iv(ticker_symbol, months=6):
    """
    Estimate historical weekly IV using realized volatility from price history.
    Since yfinance doesn't provide historical IV, we calculate realized volatility
    as a proxy and convert to weekly IV.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        
        hist = stock.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
        
        if hist.empty or len(hist) < 10:
            return pd.Series(dtype=float)
        
        # Calculate daily returns
        hist['Returns'] = hist['Close'].pct_change()
        
        # Calculate rolling 20-day realized volatility (annualized)
        hist['RealizedVol'] = hist['Returns'].rolling(window=20).std() * np.sqrt(252)
        
        # Convert to weekly IV (divide by 7)
        hist['WeeklyIV'] = hist['RealizedVol'] / 7
        
        # Resample to weekly data for cleaner plotting
        weekly_iv = hist['WeeklyIV'].resample('W').last().dropna()
        
        return weekly_iv
    except Exception:
        return pd.Series(dtype=float)


def analyze_portfolio(csv_filepath):
    try:
        # Read the portfolio data
        portfolio_df = pd.read_csv(csv_filepath)
        print(f"Successfully loaded {csv_filepath}. Fetching stock data...")
        
        # 1. FIX: Detect columns and actually use them later
        possible_ticker_cols = ['TICKER','Ticker','ticker','SYMBOL','Symbol','symbol']
        possible_shares_cols = ['POSITION','Position','position','SHARES','Shares','shares','QTY','Qty','qty']
        
        ticker_col = next((c for c in portfolio_df.columns if c in possible_ticker_cols), None)
        shares_col = next((c for c in portfolio_df.columns if c in possible_shares_cols), None)
        
        if ticker_col is None or shares_col is None:
            print("Error: Could not find ticker or shares column. Available:", list(portfolio_df.columns))
            return
            
    except FileNotFoundError:
        print(f"Error: The file '{csv_filepath}' was not found.")
        return

    prices = []
    market_values = []
    betas = []
    weekly_ivs = []

    # --- Data Fetching ---
    print(f"Processing {len(portfolio_df)} positions...")
    
    for index, row in portfolio_df.iterrows():
        # 2. FIX: Use the detected column names, not hardcoded 'TICKER'
        ticker_symbol = row[ticker_col]
        # 3. FIX: Allow fractional shares by using float, not int
        position_shares = float(row[shares_col]) 
        
        try:
            stock = yf.Ticker(ticker_symbol)
            # Fast info retrieval; 'fast_info' is often faster/more reliable in newer yfinance versions
            # but sticking to .info for compatibility with your existing logic structure
            info = stock.info 
            
            # Get current price
            price = info.get('regularMarketPrice', info.get('currentPrice', info.get('previousClose', 0.0)))
            
            if price == 0:
                print(f"  ! Warning: Could not fetch price for {ticker_symbol}")

            beta = info.get('beta', 1)
            # Handle case where beta is explicitly None (common in ETFs)
            if beta is None: 
                beta = 1.0

            weekly_iv = get_weekly_iv(stock, price)

            # 4. FIX: Do NOT cast price to int. Keep precision.
            prices.append(price) 
            betas.append(beta)
            weekly_ivs.append(weekly_iv)
            market_values.append(price * position_shares)

            print(f"  - {ticker_symbol}: ${price:.2f}")

        except Exception as e:
            print(f"  ! Error fetching {ticker_symbol}: {e}")
            prices.append(0.0)
            betas.append(1.0)
            weekly_ivs.append(np.nan)
            market_values.append(0.0)

    # Add data to DataFrame
    portfolio_df['Current Price'] = prices
    portfolio_df['Market Value'] = market_values
    portfolio_df['Beta (Risk)'] = betas
    portfolio_df['Weekly IV'] = weekly_ivs

    # Drop rows where fetch failed (Price 0) to prevent graph errors
    portfolio_df = portfolio_df[portfolio_df['Market Value'] > 0].copy()

    total_portfolio_value = portfolio_df['Market Value'].sum()
    
    # Calculate weighted average beta
    portfolio_df['Weight'] = portfolio_df['Market Value'] / total_portfolio_value
    weighted_avg_beta = (portfolio_df['Beta (Risk)'] * portfolio_df['Weight']).sum()
    print(f"\nPortfolio Weighted Average Beta: {weighted_avg_beta:.2f}")
    
    # Calculate weighted average weekly IV (excluding NaN values)
    valid_iv_mask = portfolio_df['Weekly IV'].notna()
    if valid_iv_mask.any():
        iv_weights = portfolio_df.loc[valid_iv_mask, 'Weight'] / portfolio_df.loc[valid_iv_mask, 'Weight'].sum()
        weighted_avg_iv = (portfolio_df.loc[valid_iv_mask, 'Weekly IV'] * iv_weights).sum()
        weighted_avg_iv_pct = weighted_avg_iv * 100
        print(f"Portfolio Weighted Average Weekly IV: {weighted_avg_iv_pct:.2f}%")
    else:
        weighted_avg_iv_pct = float('nan')
        print("Portfolio Weighted Average Weekly IV: N/A")
    
    # --- Visualization ---
    # print("\nGenerating visualization...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    iv_display = f'{weighted_avg_iv_pct:.2f}%' if not np.isnan(weighted_avg_iv_pct) else 'N/A'
    fig.suptitle(f'Portfolio Analysis (Total: ${total_portfolio_value:,.2f}) | Weighted Avg Beta: {weighted_avg_beta:.2f} | Weighted Avg Weekly IV: {iv_display}', fontsize=18)

    # 1. Pie Chart
    valid_ivs = portfolio_df['Weekly IV'].fillna(0)  # Replace NaN with 0 for coloring
    norm = mcolors.Normalize(vmin=valid_ivs.min(), vmax=valid_ivs.max())
    cmap = cm.viridis
    colors = [cmap(norm(iv)) for iv in valid_ivs]

    wedges, texts, autotexts = ax1.pie(
        portfolio_df['Market Value'],
        labels=portfolio_df[ticker_col], # Use dynamic col name
        autopct='%1.1f%%',
        startangle=140,
        pctdistance=0.85,
        colors=colors,
        wedgeprops=dict(width=0.4, edgecolor='#1a1a1a')
    )
    plt.setp(autotexts, size=10, weight="bold", color="white")
    ax1.set_title('Allocation by Risk (Color = Weekly IV)', fontsize=14, color='white')

    # Colorbar
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax1, orientation='vertical', fraction=0.03, pad=0.05)
    cbar.set_label('Weekly IV', fontsize=12, color='white')

    # 2. Data Table
    ax2.axis('off')
    
    # Prepare Display Data
    # 5. FIX: Explicitly select only the columns we want to show.
    # If the CSV has extra columns (like "Date"), it would break the fixed colWidths below.
    display_cols = [ticker_col, shares_col, 'Current Price', 'Market Value', 'Beta (Risk)', 'Weekly IV']
    df_display = portfolio_df[display_cols].copy()

    # Calculate Percentage
    df_display['Percentage'] = (df_display['Market Value'] / total_portfolio_value) * 100
    df_display = df_display.sort_values(by='Percentage', ascending=False)

    # Formatting
    df_display['Percentage'] = df_display['Percentage'].map('{:.2f}%'.format)
    df_display['Current Price'] = df_display['Current Price'].map('${:,.2f}'.format)
    df_display['Market Value'] = df_display['Market Value'].map('${:,.2f}'.format)
    df_display['Beta (Risk)'] = df_display['Beta (Risk)'].map('{:.2f}'.format)
    df_display['Weekly IV'] = df_display['Weekly IV'].map(lambda x: 'N/A' if pd.isna(x) else '{:.2f}%'.format(x * 100))

    # Rename columns for cleaner table header (standardize names)
    df_display.columns = ['Ticker', 'Shares', 'Price', 'Value', 'Beta', 'Weekly IV', '%']

    table = ax2.table(
        cellText=df_display.values,
        colLabels=df_display.columns,
        loc='center',
        cellLoc='left',
        # Adjusted widths to match the 7 final columns
        colWidths=[0.14, 0.12, 0.14, 0.18, 0.12, 0.16, 0.14] 
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 1.2)

    # Header Styling
    for (i, j), cell in table.get_celld().items():
        if i == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#1f77b4')
        else:
            cell.set_facecolor('#2a2a2a')
            cell.set_text_props(color='white')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save output
    output_path = os.path.join(os.path.dirname(csv_filepath) or '.', 'portfolio_analysis.csv')
    portfolio_df.to_csv(output_path, index=False)
    print(f"Analysis saved to {output_path}")
    
    # Save plot to file instead of showing (for subprocess compatibility)
    plot_path = os.path.join(os.path.dirname(csv_filepath) or '.', 'portfolio_analysis.png')
    plt.savefig(plot_path, dpi=100, bbox_inches='tight')
    print(f"Plot saved to {plot_path}")
    
    # --- Historical IV Graph ---
    print("\nFetching historical IV data for the past 6 months...")
    
    # Collect historical IV for each stock
    historical_iv_data = {}
    for ticker in portfolio_df[ticker_col].values:
        print(f"  - Fetching historical IV for {ticker}...")
        iv_series = get_historical_iv(ticker, months=6)
        if not iv_series.empty:
            historical_iv_data[ticker] = iv_series
    
    if historical_iv_data:
        # Create a DataFrame with all historical IVs
        iv_df = pd.DataFrame(historical_iv_data)
        
        # Calculate weighted portfolio IV
        weights = portfolio_df.set_index(ticker_col)['Weight']
        
        # Only use stocks that have historical data
        available_tickers = [t for t in weights.index if t in iv_df.columns]
        if available_tickers:
            # Normalize weights for available tickers
            available_weights = weights[available_tickers]
            available_weights = available_weights / available_weights.sum()
            
            # Calculate weighted portfolio IV
            portfolio_iv = pd.Series(0.0, index=iv_df.index)
            for ticker in available_tickers:
                portfolio_iv += iv_df[ticker].fillna(0) * available_weights[ticker]
            
            # Create the historical IV plot
            fig2, ax3 = plt.subplots(figsize=(14, 8))
            fig2.suptitle('Historical Weekly IV (Last 6 Months)', fontsize=18)
            
            lines = []
            labels = []
            
            # Plot portfolio weighted IV (thicker line)
            line, = ax3.plot(portfolio_iv.index, portfolio_iv.values * 100, 
                           linewidth=3, label='Portfolio (Weighted)', color='white', linestyle='--')
            lines.append(line)
            labels.append('Portfolio (Weighted)')
            
            # Plot individual stock IVs (hidden by default)
            colors = plt.cm.tab10(np.linspace(0, 1, len(iv_df.columns)))
            for idx, ticker in enumerate(iv_df.columns):
                line, = ax3.plot(iv_df.index, iv_df[ticker].values * 100, 
                               linewidth=1.5, label=ticker, color=colors[idx], alpha=0.7,
                               visible=False)  # Hidden by default
                lines.append(line)
                labels.append(ticker)
            
            ax3.set_xlabel('Date', fontsize=12, color='white')
            ax3.set_ylabel('Weekly IV (%)', fontsize=12, color='white')
            ax3.grid(True, alpha=0.3)
            
            # Create interactive legend with pick events
            leg = ax3.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
            
            # Map legend lines to original lines
            lined = {}
            for idx, (legline, origline) in enumerate(zip(leg.get_lines(), lines)):
                legline.set_picker(5)  # 5 pts tolerance
                lined[legline] = origline
                # Dim legend items for hidden lines (all except portfolio)
                if idx > 0:  # Skip portfolio line (first one)
                    legline.set_alpha(0.2)
            
            # Store visibility state
            def on_pick(event):
                legline = event.artist
                origline = lined[legline]
                visible = not origline.get_visible()
                origline.set_visible(visible)
                legline.set_alpha(1.0 if visible else 0.2)
                fig2.canvas.draw()
            
            fig2.canvas.mpl_connect('pick_event', on_pick)
            
            plt.tight_layout(rect=[0, 0, 0.85, 0.96])
            
            # Save the historical IV plot (static PNG)
            iv_plot_path = os.path.join(os.path.dirname(csv_filepath) or '.', 'portfolio_iv_history.png')
            plt.savefig(iv_plot_path, dpi=100, bbox_inches='tight')
            print(f"Historical IV plot saved to {iv_plot_path}")
            
            # Create interactive Plotly HTML version
            fig_plotly = go.Figure()
            
            # Add portfolio weighted IV line (visible by default)
            fig_plotly.add_trace(go.Scatter(
                x=portfolio_iv.index,
                y=portfolio_iv.values * 100,
                mode='lines',
                name='Portfolio (Weighted)',
                line=dict(color='white', width=3, dash='dash'),
                visible=True
            ))
            
            # Add individual stock IV lines (hidden by default - use 'legendonly')
            plotly_colors = [
                '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
            ]
            for idx, ticker in enumerate(iv_df.columns):
                fig_plotly.add_trace(go.Scatter(
                    x=iv_df.index,
                    y=iv_df[ticker].values * 100,
                    mode='lines',
                    name=ticker,
                    line=dict(color=plotly_colors[idx % len(plotly_colors)], width=1.5),
                    visible='legendonly'  # Hidden by default, click legend to show
                ))
            
            fig_plotly.update_layout(
                title='Historical Weekly IV (Last 6 Months) - Click legend items to show/hide',
                xaxis_title='Date',
                yaxis_title='Weekly IV (%)',
                template='plotly_dark',
                legend=dict(
                    yanchor='top',
                    y=0.99,
                    xanchor='left',
                    x=1.02
                ),
                hovermode='x unified'
            )
            
            # Save interactive HTML
            iv_html_path = os.path.join(os.path.dirname(csv_filepath) or '.', 'portfolio_iv_history.html')
            fig_plotly.write_html(iv_html_path, include_plotlyjs=True, full_html=True)
            print(f"Interactive IV plot saved to {iv_html_path}")
            print("\nNote: Open the HTML file in a browser for full interactivity. Click legend items to show/hide lines.")
            
            # Show interactive matplotlib plot
            plt.show()
        else:
            print("Could not calculate portfolio historical IV - no matching data.")
    else:
        print("Could not fetch historical IV data for any stocks.")

if __name__ == '__main__':
    # Ensure this file exists in your folder!
    PORTFOLIO_FILE = 'Positions_main.csv' 
    analyze_portfolio(PORTFOLIO_FILE)