"""
FRED Data Fetcher - Consumer Credit Delinquency Risk Analysis
=============================================================
신용위원회 보고서를 위한 FRED 데이터 수집 스크립트

수집 데이터:
- TOTALSL: 소비자 신용 총액
- DRCCLACBS: 소비자 대출 연체율
- UNRATE: 실업률
- FEDFUNDS: 기준금리
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
OUTPUT_DIR = Path(__file__).parent / "data" / "fred"

# 수집할 FRED 시리즈
SERIES_CONFIG = {
    "TOTALSL": {
        "name": "Total Consumer Credit Outstanding",
        "name_kr": "소비자 신용 총액",
        "unit": "Billions of Dollars",
        "frequency": "Monthly"
    },
    "DRCCLACBS": {
        "name": "Delinquency Rate on Consumer Loans",
        "name_kr": "소비자 대출 연체율",
        "unit": "Percent",
        "frequency": "Quarterly"
    },
    "UNRATE": {
        "name": "Unemployment Rate",
        "name_kr": "실업률",
        "unit": "Percent",
        "frequency": "Monthly"
    },
    "FEDFUNDS": {
        "name": "Federal Funds Effective Rate",
        "name_kr": "연방기금 금리",
        "unit": "Percent",
        "frequency": "Monthly"
    }
}


def fetch_series(series_id: str, start_date: str = "2000-01-01") -> pd.DataFrame:
    """FRED에서 단일 시리즈 데이터 수집"""

    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": datetime.now().strftime("%Y-%m-%d")
    }

    config = SERIES_CONFIG[series_id]
    print(f"  Fetching {series_id}: {config['name_kr']}...")

    response = requests.get(FRED_BASE_URL, params=params)
    response.raise_for_status()

    data = response.json().get("observations", [])
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df[["date", "value"]].rename(columns={"value": series_id})

    print(f"    -> {len(df)} observations ({df['date'].min():%Y-%m} ~ {df['date'].max():%Y-%m})")
    return df


def main():
    print("=" * 60)
    print("FRED Data Fetcher - 소비자 신용 연체 리스크 분석")
    print("=" * 60)

    if not FRED_API_KEY:
        print("Error: FRED_API_KEY not found in .env file")
        return

    # 데이터 수집
    print("\n[1/3] FRED 데이터 수집 중...")
    dataframes = {}
    for series_id in SERIES_CONFIG:
        dataframes[series_id] = fetch_series(series_id)

    # 데이터 병합 (월별 기준, 분기 데이터는 forward fill)
    print("\n[2/3] 데이터 병합 중...")
    merged = dataframes["UNRATE"][["date"]].copy()
    for series_id, df in dataframes.items():
        merged = merged.merge(df, on="date", how="left")
    merged = merged.ffill()
    print(f"    -> 병합 완료: {len(merged)} rows, {len(merged.columns)} columns")

    # 저장
    print("\n[3/3] 데이터 저장 중...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 통합 CSV 저장
    csv_path = OUTPUT_DIR / "consumer_credit_risk_data.csv"
    merged.to_csv(csv_path, index=False)
    print(f"    -> {csv_path}")

    # 메타데이터 JSON 저장
    metadata = {
        "source": "Federal Reserve Economic Data (FRED)",
        "fetch_date": datetime.now().isoformat(),
        "period": f"{merged['date'].min():%Y-%m-%d} ~ {merged['date'].max():%Y-%m-%d}",
        "series": SERIES_CONFIG
    }
    json_path = OUTPUT_DIR / "consumer_credit_risk_metadata.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"    -> {json_path}")

    # 요약 통계
    print("\n" + "=" * 60)
    print("Summary Statistics")
    print("=" * 60)
    print(merged.describe().round(2).to_string())

    print("\n" + "=" * 60)
    print("완료! 데이터가 ./data/fred/ 폴더에 저장되었습니다.")
    print("=" * 60)


if __name__ == "__main__":
    main()
