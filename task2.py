import csv
import os

# Sample mock current market prices for demonstration
CURRENT_PRICES = {
    "AAPL": 185.50,
    "MSFT": 420.00,
    "GOOGL": 175.25,
    "AMZN": 180.00,
    "TSLA": 170.50,
    "NVDA": 880.00,
    "META": 490.00
}

def get_current_price(ticker):
    """Retrieves current price or returns a default baseline if not in mock data."""
    ticker = ticker.upper()
    return CURRENT_PRICES.get(ticker, 125.00)

def main():
    print("========================================")
    print("    STOCK PORTFOLIO PERFORMANCE TRACKER ")
    print("========================================")
    
    portfolio = []
    
    print("\nEnter your portfolio positions. Type 'DONE' when finished.")
    while True:
        ticker = input("Enter ticker symbol (e.g., AAPL): ").strip().upper()
        if ticker == 'DONE':
            break
        if not ticker:
            continue
            
        try:
            buy_price = float(input(f"Enter buy price for {ticker} ($): "))
            shares = float(input(f"Enter quantity of shares for {ticker}: "))
        except ValueError:
            print("❌ Invalid number entered. Please enter valid numeric values.\n")
            continue
            
        current_price = get_current_price(ticker)
        portfolio.append({
            "ticker": ticker,
            "buy_price": buy_price,
            "shares": shares,
            "current_price": current_price
        })
        
        cont = input("Add another stock? (y/n): ").strip().lower()
        if cont != 'y':
            break

    # Fallback to sample data if nothing entered
    if not portfolio:
        print("\nNo entries provided. Loading default sample portfolio...")
        portfolio = [
            {"ticker": "AAPL", "buy_price": 150.00, "shares": 10, "current_price": CURRENT_PRICES["AAPL"]},
            {"ticker": "MSFT", "buy_price": 380.00, "shares": 5, "current_price": CURRENT_PRICES["MSFT"]},
            {"ticker": "NVDA", "buy_price": 600.00, "shares": 4, "current_price": CURRENT_PRICES["NVDA"]}
        ]

    csv_filename = "portfolio_summary.csv"
    fieldnames = ["Ticker", "Shares", "Buy Price ($)", "Current Price ($)", "Total Invested ($)", "Current Value ($)", "Gain/Loss ($)", "Gain/Loss (%)"]
    
    summary_rows = []
    total_invested_portfolio = 0.0
    total_value_portfolio = 0.0

    print("\n" + "="*85)
    print(f"{'Ticker':<8} {'Shares':<8} {'Buy ($)':<10} {'Current ($)':<12} {'Invested ($)':<14} {'Value ($)':<12} {'Gain/Loss':<12}")
    print("="*85)

    for pos in portfolio:
        ticker = pos["ticker"]
        shares = pos["shares"]
        buy = pos["buy_price"]
        current = pos["current_price"]
        
        invested = shares * buy
        value = shares * current
        gain_loss_dollar = value - invested
        gain_loss_pct = (gain_loss_dollar / invested * 100) if invested > 0 else 0.0
        
        total_invested_portfolio += invested
        total_value_portfolio += value
        
        print(f"{ticker:<8} {shares:<8.2f} {buy:<10.2f} {current:<12.2f} {invested:<14.2f} {value:<12.2f} {gain_loss_dollar:+10.2f} ({gain_loss_pct:+.2f}%)")
        
        summary_rows.append({
            "Ticker": ticker,
            "Shares": shares,
            "Buy Price ($)": round(buy, 2),
            "Current Price ($)": round(current, 2),
            "Total Invested ($)": round(invested, 2),
            "Current Value ($)": round(value, 2),
            "Gain/Loss ($)": round(gain_loss_dollar, 2),
            "Gain/Loss (%)": f"{gain_loss_pct:.2f}%"
        })

    total_gain_loss = total_value_portfolio - total_invested_portfolio
    total_gain_loss_pct = (total_gain_loss / total_invested_portfolio * 100) if total_invested_portfolio > 0 else 0.0

    print("="*85)
    print(f"Total Invested:         ${total_invested_portfolio:,.2f}")
    print(f"Total Portfolio Value:  ${total_value_portfolio:,.2f}")
    print(f"Total Gain/Loss:        ${total_gain_loss:+,.2f} ({total_gain_loss_pct:+.2f}%)")
    print("="*85)

    # Write results into CSV
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)
            
    print(f"\n📁 Portfolio summary successfully exported to '{csv_filename}'.")

if __name__ == "__main__":
    main()