# Canadian Housing Intelligence Platform

An end-to-end data engineering pipeline integrating housing, economic, and demographic data across 5 major Canadian cities to analyze affordability, housing supply, and market trends.

## Overview

This project answers real questions a housing policy analyst or city planner might ask:

- Which cities are becoming less affordable over time?
- Does population growth outpace housing construction?
- How do interest rate changes correlate with housing prices?
- Which cities have the tightest rental vacancy rates?

## Architecture

```
Bank of Canada (API) + CMHC (rental reports) + StatCan (population API)
        │
        ▼
   Python (requests, pandas) ── ingest, standardize city names
        │
        ▼
   Azurite (local Azure Blob Storage emulator) ── raw data lake
        │
        ▼
   PostgreSQL ── star schema warehouse (dim_city, dim_date, fact_housing_metrics)
        │
        ▼
   dbt ── SQL transformation layer: staging + mart models with window functions
        │
        ▼
   Power BI ── 3-page interactive dashboard
```

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Ingestion | Python, requests, pandas | Pull from Bank of Canada's Valet API, StatCan's Table API, and CMHC rental reports |
| Object storage | Azurite (Azure Blob emulator) | Durable raw storage, mirrors real Azure Storage's API |
| Data warehouse | PostgreSQL (Docker) | Star schema: city and date dimensions, housing metrics fact table |
| Transformation | dbt | Version-controlled SQL models — staging layer + business-logic marts |
| Visualization | Power BI | 3-page interactive dashboard connected live to Postgres |

## Data Sources

- **Bank of Canada** — Valet API, Bank Rate series (V39079), 2009–2024, 4,509 observations. No auth required.
- **CMHC** — Primary Rental Market Statistics, Oct-22 through Oct-25, 5 cities (Toronto, Montreal, Vancouver, Calgary, Ottawa), transcribed from official PDF reports (see data quality notes below).
- **Statistics Canada** — Table 17-10-0135-01, population estimates by Census Metropolitan Area, 2001–2022.

**Data quality notes** (documented honestly, not hidden):
- CMHC publishes rental market statistics as formatted PDF reports rather than a queryable API. Given the small number of cities tracked (5), values were manually transcribed directly from the official PDFs rather than parsed with a table-extraction library — printable reports interleave reliability-code letters (e.g. `4.6 d`) between numeric columns in a way that makes automated extraction unreliable at this scale.
- StatCan's geography names required exact matching to their official Census Metropolitan Area naming (e.g. `"Toronto (CMA), Ontario"`, `"Ottawa - Gatineau (CMA), Ontario/Quebec"`) — resolved by inspecting the source data directly rather than guessing.
- All city names were standardized to a plain form (Toronto, Montreal, Vancouver, Calgary, Ottawa) across sources so they join correctly in the warehouse.
- **Population data (2001–2022) and housing supply data (2022–2025) only overlap in a single year (2022)**, so a single combined "supply vs. demand gap" metric isn't reliably calculable. The `mart_supply_vs_demand` model instead reports both growth series independently, each computed over its own valid range — an honest choice over forcing a misleading comparison.
- Bank of Canada's interest rate is a national series and is joined to every city by year, since it doesn't vary by city.

## Pipeline Stages

1. **Ingest** — Python scripts pull each source (API calls for Bank of Canada and StatCan, transcribed data for CMHC)
2. **Standardize** — city names, date formats, and column names normalized across all 3 sources into a Silver layer
3. **Warehouse** — loaded into PostgreSQL as a star schema (`dim_city`, `dim_date`, `fact_housing_metrics`), built idempotently (`TRUNCATE` before reload to prevent duplicate inserts on repeated runs)
4. **Transform** — dbt models: a staging layer (`stg_fact_housing`) joining fact + dimensions, and 3 mart models using CTEs and window functions (`LAG`, `RANK`) for year-over-year growth and affordability ranking
5. **Visualize** — Power BI connects live to Postgres, importing the 4 dbt models directly

## Dashboard

![Housing Intelligence Dashboard](./dashboards/dashboard_screenshot.png)

### Dashboard Pages

**Page 1 — Overview**
*(screenshot: `./dashboards/page1_overview.png`)*
KPI cards (cities tracked, average rent, latest data year), a bar chart ranking cities by average rent in the most recent year, and a line chart showing each city's rent trend over time. Answers "which cities are becoming less affordable?"

**Page 2 — Deep Dive**
*(screenshot: `./dashboards/page2_deep_dive.png`)*
A population-growth-vs-housing-supply-growth line chart (filterable by city via slicer) and a vacancy rate comparison bar chart. Answers "does population growth outpace construction?" and "which cities have the tightest vacancy rates?"

**Page 3 — Insights**
*(screenshot: `./dashboards/page3_insights.png`)*
Interest rate vs. rent trend line chart (filterable by city) plus a written insights summary covering the key findings below. Answers "how do interest rates correlate with housing prices, and what should a reader take away?"

## Key Findings

- **Vancouver is consistently the least affordable city** in the dataset (highest average rent), while **Montreal is consistently the most affordable**.
- **Calgary saw the sharpest single-year rent increase** (~10% in one year) despite not being the most expensive city overall — a signal of rapid change, distinct from persistently high cost.
- **Population growth nearly stalled in 2021** (0.05% in Toronto) during pandemic-era border restrictions, then rebounded to over 2% growth by 2022 — an independently-verified real-world pattern the data reproduces correctly.
- **Housing supply did not keep pace with demand in at least one major market**: Toronto's rental unit count shrank 0.49% in 2023, even as population had been growing steadily through 2022.
- **Vancouver has the tightest rental market** (lowest vacancy rate, ~1.5%), while **Calgary has the most availability** (~3.5% vacancy).

## Setup

See `/src` for ingestion and warehouse-loading scripts, `/sql` for the schema definition, and `/dbt/housing_dbt` for the dbt project (staging and mart models). Requires Docker (for PostgreSQL and Azurite) and a Postgres connection configured in `dbt/housing_dbt/housing_dbt/profiles.yml`.
