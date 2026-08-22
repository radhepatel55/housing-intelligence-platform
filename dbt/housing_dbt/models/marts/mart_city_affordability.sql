WITH yearly_data AS (
    SELECT
        city_name,
        year,
        avg_rent,
        vacancy_rate,
        interest_rate,
        LAG(avg_rent) OVER (PARTITION BY city_name ORDER BY year) AS prev_year_rent
    FROM {{ ref('stg_fact_housing') }}
    WHERE avg_rent IS NOT NULL
)

SELECT
    city_name,
    year,
    avg_rent,
    vacancy_rate,
    interest_rate,
    prev_year_rent,
    ROUND(((avg_rent - prev_year_rent) / prev_year_rent * 100)::numeric, 2) AS rent_growth_pct,
    RANK() OVER (PARTITION BY year ORDER BY avg_rent DESC) AS affordability_rank
FROM yearly_data
ORDER BY city_name, year