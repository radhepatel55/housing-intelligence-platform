WITH pop_growth AS (
    SELECT
        city_name,
        year,
        population,
        LAG(population) OVER (PARTITION BY city_name ORDER BY year) AS prev_year_population
    FROM {{ ref('stg_fact_housing') }}
    WHERE population IS NOT NULL
)

SELECT
    city_name,
    year,
    population,
    prev_year_population,
    ROUND(((population - prev_year_population)::numeric / prev_year_population * 100), 2) AS population_growth_pct
FROM pop_growth
WHERE prev_year_population IS NOT NULL
ORDER BY city_name, year