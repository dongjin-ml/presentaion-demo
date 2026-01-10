"""
FRED Data Fetcher - Consumer Credit Delinquency Risk Analysis
=============================================================
신용위원회 미팅용 리스크 모니터링 보고서 데이터 수집 스크립트

수집 데이터:
- DRCCLACBS: 소비자 대출 연체율
- UNRATE: 실업률
- FEDFUNDS: 기준금리
- TOTALSL: 소비자 신용 총액

분석 목적:
1. 현재 소비자 대출 연체율이 정상 범위인가?
2. 실업률, 금리 등 선행지표에 경고 신호가 있는가?
3. 2008년, 2020년 위기 직전 수준과 비교하면?
4. 빨간불/노란불/초록불 종합 평가
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# 환경변수 로드
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
OUTPUT_DIR = PROJECT_ROOT / "data" / "fred"

# 수집할 FRED 시리즈 (컬럼 설명 포함)
SERIES_CONFIG = {
    "DRCCLACBS": {
        "name": "Delinquency Rate on Consumer Loans, All Commercial Banks",
        "name_kr": "소비자 대출 연체율",
        "unit": "Percent",
        "frequency": "Quarterly",
        "description": "상업은행의 소비자 대출 연체율 (90일 이상 연체 비율). 높을수록 소비자 신용 리스크 증가.",
        "risk_threshold": {
            "green": "< 3.0%",
            "yellow": "3.0% - 4.5%",
            "red": "> 4.5%"
        },
        "historical_crisis": {
            "2008_peak": "6.77% (2009-Q4)",
            "2020_peak": "2.53% (2020-Q2)"
        }
    },
    "UNRATE": {
        "name": "Unemployment Rate",
        "name_kr": "실업률",
        "unit": "Percent",
        "frequency": "Monthly",
        "description": "미국 전체 실업률 (계절 조정). 경기침체 선행지표로 높을수록 소비자 신용 상환 능력 저하.",
        "risk_threshold": {
            "green": "< 5.0%",
            "yellow": "5.0% - 7.0%",
            "red": "> 7.0%"
        },
        "historical_crisis": {
            "2008_peak": "10.0% (2009-10)",
            "2020_peak": "14.7% (2020-04)"
        }
    },
    "FEDFUNDS": {
        "name": "Federal Funds Effective Rate",
        "name_kr": "연방기금 금리",
        "unit": "Percent",
        "frequency": "Monthly",
        "description": "연방준비제도 기준금리 (실효금리). 급격한 인상은 차입 비용 증가로 연체 가능성 상승.",
        "risk_threshold": {
            "green": "< 3.0%",
            "yellow": "3.0% - 5.0%",
            "red": "> 5.0%"
        },
        "historical_crisis": {
            "2008_before": "5.25% (2007)",
            "2020_before": "1.58% (2020-03)"
        }
    },
    "TOTALSL": {
        "name": "Total Consumer Credit Outstanding",
        "name_kr": "소비자 신용 총액",
        "unit": "Billions of Dollars",
        "frequency": "Monthly",
        "description": "미국 전체 소비자 신용 잔액 (계절 조정). 급증 시 과도한 레버리지 우려.",
        "risk_threshold": {
            "note": "절대값보다 증가율(YoY)로 평가"
        },
        "historical_crisis": {
            "2008_level": "$2,573B (2008-09)",
            "2020_level": "$4,197B (2020-02)"
        }
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
    df = df.dropna()

    print(f"     -> {len(df)} observations ({df['date'].min():%Y-%m} ~ {df['date'].max():%Y-%m})")
    return df


def main():
    print("=" * 70)
    print("FRED Data Fetcher - 신용위원회 미팅용 리스크 모니터링 보고서")
    print("=" * 70)

    if not FRED_API_KEY:
        print("❌ Error: FRED_API_KEY not found in .env file")
        return

    # 데이터 수집
    print("\n[1/3] FRED 데이터 수집 중...")
    dataframes = {}
    for series_id in SERIES_CONFIG:
        try:
            dataframes[series_id] = fetch_series(series_id)
        except Exception as e:
            print(f"     ❌ Error fetching {series_id}: {e}")
            return

    # 데이터 병합 (월별 기준, 분기 데이터는 forward fill)
    print("\n[2/3] 데이터 병합 중...")
    merged = dataframes["UNRATE"][["date"]].copy()
    for series_id, df in dataframes.items():
        merged = merged.merge(df, on="date", how="left")
    merged = merged.ffill()
    print(f"     -> 병합 완료: {len(merged)} rows, {len(merged.columns)-1} indicators")

    # 저장
    print("\n[3/3] 데이터 저장 중...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 통합 CSV 저장
    csv_path = OUTPUT_DIR / "consumer_credit_risk_data.csv"
    merged.to_csv(csv_path, index=False)
    print(f"     ✓ 데이터: {csv_path}")

    # 최신 값 추출
    latest_row = merged.iloc[-1]
    latest_values = {
        series_id: {
            "value": float(latest_row[series_id]),
            "date": latest_row["date"].strftime("%Y-%m-%d"),
            "unit": SERIES_CONFIG[series_id]["unit"]
        }
        for series_id in SERIES_CONFIG.keys()
    }

    # 메타데이터 JSON 저장
    metadata = {
        "purpose": "신용위원회 미팅용 리스크 모니터링 보고서",
        "source": "Federal Reserve Economic Data (FRED)",
        "api_url": "https://fred.stlouisfed.org/",
        "fetch_date": datetime.now().isoformat(),
        "data_period": {
            "start": merged["date"].min().strftime("%Y-%m-%d"),
            "end": merged["date"].max().strftime("%Y-%m-%d"),
            "observations": len(merged)
        },
        "analysis_requirements": [
            "1. 현재 소비자 대출 연체율이 정상 범위인가?",
            "2. 실업률, 금리 등 선행지표에 경고 신호가 있는가?",
            "3. 2008년, 2020년 위기 직전 수준과 비교하면?",
            "4. 빨간불/노란불/초록불 종합 평가"
        ],
        "series": SERIES_CONFIG,
        "latest_values": latest_values,
        "data_file": str(csv_path.name)
    }

    json_path = OUTPUT_DIR / "metadata.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"     ✓ 메타데이터: {json_path}")

    # 최신 값 출력
    print("\n" + "=" * 70)
    print("최신 데이터 (Latest Values)")
    print("=" * 70)
    for series_id, config in SERIES_CONFIG.items():
        val_info = latest_values[series_id]
        print(f"  • {config['name_kr']}: {val_info['value']:.2f} {val_info['unit']} ({val_info['date']})")

    print("\n" + "=" * 70)
    print("✓ 완료! 데이터가 ./data/fred/ 폴더에 저장되었습니다.")
    print("=" * 70)
    print(f"\n📊 데이터 파일: {csv_path}")
    print(f"📋 메타데이터: {json_path}")


if __name__ == "__main__":
    main()
