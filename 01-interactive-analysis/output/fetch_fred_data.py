"""
FRED Data Fetcher - Consumer Credit Risk Analysis
==================================================
Credit committee meeting risk monitoring report data collection script

Datasets:
- TOTALSL: Total Consumer Credit Outstanding
- DRCCLACBS: Delinquency Rate on Credit Card Loans
- UNRATE: Unemployment Rate
- FEDFUNDS: Federal Funds Effective Rate
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
OUTPUT_DIR = PROJECT_ROOT / "data" / "fred"

# FRED series configuration with metadata
SERIES_CONFIG = {
    "TOTALSL": {
        "name": "Total Consumer Credit Outstanding",
        "unit": "Millions of Dollars",
        "frequency": "Monthly",
        "description": "Total consumer credit outstanding, seasonally adjusted. Includes revolving and nonrevolving credit."
    },
    "DRCCLACBS": {
        "name": "Delinquency Rate on Credit Card Loans, All Commercial Banks",
        "unit": "Percent",
        "frequency": "Quarterly",
        "description": "Delinquency rate on credit card loans at all commercial banks. Loans 30+ days past due."
    },
    "UNRATE": {
        "name": "Unemployment Rate",
        "unit": "Percent",
        "frequency": "Monthly",
        "description": "Civilian unemployment rate, seasonally adjusted. Key indicator of labor market health."
    },
    "FEDFUNDS": {
        "name": "Federal Funds Effective Rate",
        "unit": "Percent",
        "frequency": "Monthly",
        "description": "Effective federal funds rate. The interest rate at which depository institutions lend reserve balances to other depository institutions overnight."
    }
}


def fetch_series(series_id: str, start_date: str = "2000-01-01") -> pd.DataFrame:
    """Fetch a single series from FRED API"""
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": datetime.now().strftime("%Y-%m-%d")
    }

    config = SERIES_CONFIG[series_id]
    print(f"  Fetching {series_id}: {config['name']}...")

    response = requests.get(FRED_BASE_URL, params=params)
    response.raise_for_status()

    data = response.json().get("observations", [])
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df[["date", "value"]].rename(columns={"value": series_id})
    df = df.dropna()

    print(f"     -> {len(df)} observations ({df['date'].min():%Y-%m} ~ {df['date'].max():%Y-%m})")
    return df


def main():
    print("=" * 70)
    print("FRED Data Fetcher - Consumer Credit Risk Report")
    print("=" * 70)

    if not FRED_API_KEY:
        print("Error: FRED_API_KEY not found in .env file")
        return

    # Fetch data
    print("\n[1/3] Fetching FRED data...")
    dataframes = {}
    for series_id in SERIES_CONFIG:
        try:
            dataframes[series_id] = fetch_series(series_id)
        except Exception as e:
            print(f"     Error fetching {series_id}: {e}")
            return

    # Merge data (monthly frequency, forward-fill quarterly data)
    print("\n[2/3] Merging data...")
    merged = dataframes["UNRATE"][["date"]].copy()
    for series_id, df in dataframes.items():
        merged = merged.merge(df, on="date", how="left")
    merged = merged.ffill()
    print(f"     -> Merged: {len(merged)} rows, {len(merged.columns)-1} indicators")

    # Save files
    print("\n[3/3] Saving files...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save CSV
    csv_path = OUTPUT_DIR / "consumer_credit_risk_data.csv"
    merged.to_csv(csv_path, index=False)
    print(f"     Data: {csv_path}")

    # Extract latest values
    latest_row = merged.iloc[-1]
    latest_values = {
        series_id: {
            "value": float(latest_row[series_id]),
            "date": latest_row["date"].strftime("%Y-%m-%d"),
            "unit": SERIES_CONFIG[series_id]["unit"]
        }
        for series_id in SERIES_CONFIG.keys()
    }

    # Save metadata JSON
    metadata = {
        "purpose": "Credit Risk Committee Meeting Report",
        "source": "Federal Reserve Economic Data (FRED)",
        "api_url": "https://fred.stlouisfed.org/",
        "fetch_date": datetime.now().isoformat(),
        "data_period": {
            "start": merged["date"].min().strftime("%Y-%m-%d"),
            "end": merged["date"].max().strftime("%Y-%m-%d"),
            "observations": len(merged)
        },
        "columns": {
            series_id: {
                "name": config["name"],
                "unit": config["unit"],
                "frequency": config["frequency"],
                "description": config["description"]
            }
            for series_id, config in SERIES_CONFIG.items()
        },
        "latest_values": latest_values,
        "data_file": str(csv_path.name)
    }

    json_path = OUTPUT_DIR / "consumer_credit_risk_metadata.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"     Metadata: {json_path}")

    # Print latest values
    print("\n" + "=" * 70)
    print("Latest Values")
    print("=" * 70)
    for series_id, config in SERIES_CONFIG.items():
        val_info = latest_values[series_id]
        print(f"  {series_id}: {val_info['value']:.2f} {val_info['unit']} ({val_info['date']})")

    print("\n" + "=" * 70)
    print("Done! Files saved to ./data/fred/")
    print("=" * 70)


if __name__ == "__main__":
    main()
