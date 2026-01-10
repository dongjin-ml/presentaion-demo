2번과 싱크 맞추기

1. 내가 분석하고 싶은 주제 확정하기
    - You will write a US Consumer Price Index (CPI) Inflation Analysis Report.
      Analyze from an economic and policy perspective, focusing on:
      - Inflation trends by category (Food, Energy, Housing, etc.)
      - COVID-19 impact analysis (2020 before/after)
      - Category-wise volatility comparison
      Generate charts and extract actionable insights, then create a docx file.
      The analysis target is the './data/fred/' directory.
      us-cpi-by-category.csv is the data file,
      us_cpi_by_category_columns.json contains the column definitions.

      Topic: Consumer Credit Delinquency Risk Prediction

Analysis Focus:
- Consumer credit trends (FRED: TOTALSL)
- Delinquency rates by category (FRED: DRCCLACBS)
- Unemployment impact on defaults (FRED: UNRATE)
- Interest rate sensitivity (FRED: FEDFUNDS)

Business Connection:
✓ FinTechCo's banking division issues credit
✓ Direct impact on loan portfolio risk
✓ Regulatory reporting requirement
✓ Real-time risk monitoring need

Deliverable:
- Risk dashboard for credit committee
- Early warning indicators
- Scenario analysis (recession impact)
```

**Why this works:**
```
CTO: "Yes, we need this for our credit card business"
CDO: "Our analysts do this quarterly - automating it saves time"
Head of DT: "This is exactly the kind of analysis we want to democratize"

2. 필요한 데이터 가지고 오라는 데모 스토리 만들기 (1번에서 클로드 코드로 보여주기)
    ---
 내일 신용위원회 미팅용 리스크 모니터링 보고서를 급하게 준비해야 해.

필요한 분석:
1. 현재 소비자 대출 연체율이 정상 범위인가?
2. 실업률, 금리 등 선행지표에 경고 신호가 있는가?
3. 2008년, 2020년 위기 직전 수준과 비교하면?
4. 빨간불/노란불/초록불 종합 평가

FRED 데이터 필요:
- DRCCLACBS: 연체율
- UNRATE: 실업률  
- FEDFUNDS: 기준금리
- TOTALSL: 소비자 신용 총액

2000년부터 최신 데이터와 그에 대한 메타데이터(컬럼설명) ./data/fred/에 저장하는 파이썬 스크립트 작성해줘.
파일은 ./output 디렉토리에 아래와 같이 저장해줘:
- python script: ./output/fetch_fred_data.py

API 키는 .env 파일의 FRED_API_KEY.

  
  이 프롬프트로 데모를 시작하면 청중이 "아, 이렇게 요청하면 되는구나"라고 바로 이해할 수 있습니다.


3. 분석을 위해 필요한 세부 엑티비티 정하는 데모 스토리 만들기 (1번에서 클로드 코드로 보여주기)
분석 플래닝 프롬프트

  데이터는 받았으니까 이제 분석해야 하는데,
일단 플랜부터 세워야겠어.

뭘 해야 하냐면:
- 어떤 지표가 연체율 예측에 좋은지 찾기
- 지금이 2008년이나 2020년 때랑 비교해서 어떤지 보기
- 리스크 신호등 기준 정하기
- 대시보드랑 임원 보고용 요약 만들기

데이터는 ./data/fred/consumer_credit_risk_data.csv에 있어.
메타데이터: ./data/fred/consumer_credit_risk_metadata.json

이거 어떤 순서로 진행하면 좋을지 단계별 플랜 짜줘.

  ---
  프롬프트 구조 설명 (발표용)
  ┌───────────────┬─────────────────────┬─────────────────────────────────┐
  │     섹션      │        목적         │            데모 효과            │
  ├───────────────┼─────────────────────┼─────────────────────────────────┤
  │ 분석 목표     │ 구체적인 질문 4가지 │ "AI가 비즈니스 질문을 이해한다" │
  ├───────────────┼─────────────────────┼─────────────────────────────────┤
  │ 원하는 아웃풋 │ 기대 결과물 명시    │ "결과물 지향적 요청"            │
  ├───────────────┼─────────────────────┼─────────────────────────────────┤
  │ 데이터 위치   │ 컨텍스트 제공       │ "이미 수집한 데이터 연결"       │
  ├───────────────┼─────────────────────┼─────────────────────────────────┤
  │ 플랜 요청     │ 액션 아이템 정리    │ "AI가 체계적으로 계획"          │
  └───────────────┴─────────────────────┴─────────────────────────────────┘




🎯 Interactive Demo Strategies for Act 1
┌─────────────────────────────────────────────────────┐
│ Act 1: Claude Code Demo (8 minutes)                 │
└─────────────────────────────────────────────────────┘

Scenario Setup (30 seconds):
"Your credit committee meets tomorrow. They need updated
delinquency risk analysis. Your analyst called in sick.
You have 20 minutes to prepare the report."

[Data Collection - 2 minutes]
- FRED: Consumer credit levels (TOTALSL)
- FRED: Delinquency rates (DRCCLACBS)  
- FRED: Unemployment (UNRATE)
- FRED: Interest rates (FEDFUNDS)

Claude Code: "Get all these datasets, align by date, 
              handle missing values"

[Analysis - 3 minutes]
- Correlation analysis
- 2008/2020 crisis pattern identification
- Current trend assessment
- Risk flag generation

Claude Code: "Show me which economic indicator is 
              the strongest predictor of delinquency"

[Visualization - 2 minutes]
- Interactive dashboard with Plotly
- Recession bands highlighted
- Current position marked
- Forecast next 6 months

Claude Code: "Create an executive dashboard that 
              shows current risk level vs historical"

[Wrap - 1 minute]
"Done. What took 3 days now takes 20 minutes.
For FinTechCo's credit team, this means..."

┌─────────────────────────────────────────────────────┐
│ Act 2: Transition (1 minute)                        │
└─────────────────────────────────────────────────────┐

"Now, what if you need this analysis:
- Every day (not just quarterly)
- For 50 loan categories (not just one)
- With automatic alerts
- Integrated with your risk system

This is where agent orchestration helps..."

┌─────────────────────────────────────────────────────┐
│ Act 3: Deep Insight (5-6 minutes)                   │
└─────────────────────────────────────────────────────┘

Show pre-built Deep Insight workflow:
- Automated daily credit risk monitoring
- Multi-category analysis
- Alert system
- Integration capabilities

"LG Electronics used this approach to reduce 
portfolio analysis from 3 days to 30 minutes.
Same principle applies to FinTechCo's credit operations."
```

---

## ⚠️ Why CPI Topic is Risky

**Attendee's Internal Dialogue:**
```
Minute 1: "Interesting topic..."
Minute 3: "Wait, why are we analyzing CPI?"
Minute 5: "We don't have economists on staff..."
Minute 7: "Is this relevant to our business?"
Minute 10: "I'm losing focus... when does this relate to us?"
```

**Your Internal Dialogue:**
```
During Q&A:
Attendee: "This is interesting, but how does CPI analysis 
          apply to our payment processing business?"

You: "Well, uh... inflation affects consumer spending,
      which... impacts payment volumes..." 😰

[Weak connection, loses credibility]