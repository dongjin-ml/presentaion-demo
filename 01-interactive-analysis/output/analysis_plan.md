# Credit Risk Analysis Plan
## Credit Committee Meeting Report

**Prepared:** 2026-01-11
**Data Period:** 2000-01 to 2025-12 (311 observations)
**Target Variable:** DRCCLACBS (Delinquency Rate on Credit Card Loans)

---

## Phase 1: Predictive Indicator Analysis

### Objective
Identify which economic indicator best predicts changes in delinquency rates.

### Methodology
1. **Lagged Correlation Analysis**
   - Calculate Pearson correlations between each predictor and DRCCLACBS
   - Test lags from 0 to 12 months (predictor leads target)
   - Identify optimal lead time for each indicator

2. **Predictors to Analyze**
   | Indicator | Description | Hypothesis |
   |-----------|-------------|------------|
   | UNRATE | Unemployment Rate | Higher unemployment -> Higher delinquency |
   | FEDFUNDS | Federal Funds Rate | Higher rates -> Higher borrowing costs -> Higher delinquency |
   | TOTALSL | Total Consumer Credit | Credit expansion may precede stress |

### Deliverables
- [ ] Correlation matrix heatmap (lags 0-12 months)
- [ ] Table: Optimal lag and correlation for each predictor
- [ ] Identification of strongest leading indicator

### Output File
`correlation_analysis.png`

---

## Phase 2: Crisis Period Comparison

### Objective
Compare current economic conditions to historical crisis periods.

### Period Definitions
| Period | Start Date | End Date | Description |
|--------|------------|----------|-------------|
| Pre-2008 Crisis | 2006-01-01 | 2007-12-31 | Baseline before financial crisis |
| 2008 Financial Crisis | 2008-01-01 | 2009-12-31 | Peak stress period |
| Pre-COVID | 2019-01-01 | 2019-12-31 | Baseline before pandemic |
| COVID Crisis | 2020-01-01 | 2020-12-31 | Pandemic shock period |
| Current | Last 6 months | Present | Current conditions |

### Metrics to Compare
For each period, calculate:
- Mean value
- Maximum value
- Minimum value
- Standard deviation

### Deliverables
- [ ] Period statistics table (all indicators)
- [ ] Current vs. pre-crisis percentage comparison
- [ ] Distance from historical peaks
- [ ] Multi-panel time series chart with crisis periods highlighted

### Output File
`crisis_comparison.png`

---

## Phase 3: Risk Signal System

### Objective
Create a traffic-light risk classification based on historical percentiles.

### Threshold Methodology
Using 25-year historical data to establish percentile-based thresholds:

| Risk Flag | Percentile Range | Interpretation | Action Level |
|-----------|------------------|----------------|--------------|
| GREEN | < 50th | Low Risk | Monitor |
| YELLOW | 50th - 75th | Moderate Risk | Watch closely |
| ORANGE | 75th - 90th | Elevated Risk | Prepare contingencies |
| RED | > 90th | High Risk | Immediate attention |

### Indicators to Flag
1. **DRCCLACBS** - Primary risk metric (delinquency rate)
2. **UNRATE** - Labor market health
3. **FEDFUNDS** - Monetary policy stress

### Composite Risk Score
- Average percentile across all flagged indicators
- Weighted option: Higher weight on delinquency rate

### Deliverables
- [ ] Threshold reference table with exact cutoff values
- [ ] Current value assessment for each indicator
- [ ] Individual risk flags (RED/YELLOW/GREEN)
- [ ] Composite risk score and overall status

### Output
Risk assessment table in dashboard

---

## Phase 4: Executive Dashboard

### Objective
Create a single-page visual summary for committee presentation.

### Dashboard Layout
```
+----------------------------------+----------------------------------+
|  CURRENT VALUES vs HISTORY       |  DELINQUENCY TREND               |
|  (Horizontal bar: percentiles)   |  (Line chart with thresholds)    |
+----------------------------------+----------------------------------+
|  PERIOD COMPARISON               |  RISK SUMMARY                    |
|  (Grouped bar chart)             |  (Text box with key findings)    |
+----------------------------------+----------------------------------+
```

### Dashboard Components

#### Panel 1: Current vs Historical Distribution
- Horizontal bars showing current percentile position
- Color-coded by risk flag
- Display actual values

#### Panel 2: Delinquency Trend with Thresholds
- Full time series of DRCCLACBS
- Horizontal lines at 50th, 75th, 90th percentiles
- Current value marker

#### Panel 3: Period Comparison
- Grouped bar chart comparing periods
- Metrics: Delinquency, Unemployment, Fed Funds

#### Panel 4: Risk Summary Box
- Current date
- Each indicator: value, percentile, flag
- Composite score
- Overall status recommendation

### Deliverables
- [ ] Executive dashboard image
- [ ] JSON file with all analysis results
- [ ] Console output with executive summary

### Output Files
- `risk_dashboard.png`
- `credit_risk_analysis_results.json`

---

## Implementation Summary

### Script Structure
```
credit_risk_analysis.py
├── Data Loading
├── Phase 1: Correlation Analysis
│   ├── Calculate lagged correlations
│   ├── Find optimal lags
│   └── Generate correlation plot
├── Phase 2: Crisis Comparison
│   ├── Define period boundaries
│   ├── Calculate period statistics
│   └── Generate comparison plot
├── Phase 3: Risk Flags
│   ├── Calculate percentile thresholds
│   ├── Assess current values
│   └── Compute composite score
├── Phase 4: Dashboard
│   ├── Create 4-panel figure
│   └── Export results
└── Executive Summary Output
```

### Dependencies
- pandas (data manipulation)
- numpy (numerical operations)
- matplotlib (visualization)
- seaborn (enhanced plots)
- scipy (statistical tests)

### Output Files
| File | Description |
|------|-------------|
| `credit_risk_analysis.py` | Main analysis script |
| `correlation_analysis.png` | Phase 1 visualization |
| `crisis_comparison.png` | Phase 2 visualization |
| `risk_dashboard.png` | Executive dashboard |
| `credit_risk_analysis_results.json` | Machine-readable results |

---

## Verification Checklist

After execution, verify:
- [ ] All 4 PNG files generated in `./output/`
- [ ] JSON results contain all analysis sections
- [ ] Visualizations render without errors
- [ ] Executive summary prints to console
- [ ] Risk flags correctly assigned based on thresholds

---

## Expected Insights

### Leading Indicator
- Identify which metric provides earliest warning
- Quantify lead time (months ahead)

### Current Risk Assessment
- Position relative to 25-year history
- Comparison to pre-crisis levels
- Overall risk classification

### Actionable Output
- Clear RED/YELLOW/GREEN signals
- Quantified distance from danger zones
- Historical context for committee discussion
