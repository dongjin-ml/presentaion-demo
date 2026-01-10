import os
from dotenv import load_dotenv
from fredapi import Fred
import pandas as pd

def main():
    load_dotenv()

    api_key = os.getenv('FRED_API_KEY')
    if not api_key:
        print("Error: FRED_API_KEY not found in .env file")
        print("Please create a .env file and add your FRED API key")
        print("Get your API key from: https://fred.stlouisfed.org/docs/api/api_key.html")
        return

    fred = Fred(api_key=api_key)

    print("Fetching consumer credit data from FRED...")
    # TOTALSL = Total Consumer Credit Outstanding
    consumer_credit = fred.get_series('TOTALSL')
    print(f"Consumer Credit Data (latest 5 values):")
    print(consumer_credit.tail())
    print(f"\nTotal records: {len(consumer_credit)}")

    print("\n" + "="*60 + "\n")

    print("Fetching unemployment data from FRED...")
    # UNRATE = Civilian Unemployment Rate
    unemployment = fred.get_series('UNRATE')
    print(f"Unemployment Rate Data (latest 5 values):")
    print(unemployment.tail())
    print(f"\nTotal records: {len(unemployment)}")

    print("\n" + "="*60 + "\n")
    print("Summary Statistics:")
    print(f"\nConsumer Credit (TOTALSL):")
    print(consumer_credit.describe())
    print(f"\nUnemployment Rate (UNRATE):")
    print(unemployment.describe())

    return consumer_credit, unemployment


if __name__ == "__main__":
    main()
