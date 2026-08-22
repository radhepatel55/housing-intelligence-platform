WITH combined AS (
    SELECT
        city_name,
        year,
        population,
        num_units,
        LAG(population) OVER (PARTITION BY city_name ORDER BY year) AS prev_population,
        LAG(num_units) OVER (PARTITION BY city_name ORDER BY year) AS prev_num_units
    FROM {{ ref('stg_fact_housing') }}
)

SELECT
    city_name,
    year,
    population,
    num_units,
    CASE WHEN prev_population IS NOT NULL
         THEN ROUND(((population - prev_population)::numeric / prev_population * 100), 2)
         END AS population_growth_pct,
    CASE WHEN prev_num_units IS NOT NULL
         THEN ROUND(((num_units - prev_num_units)::numeric / prev_num_units * 100), 2)
         END AS housing_supply_growth_pct
FROM combined
WHERE population IS NOT NULL OR num_units IS NOT NULL
ORDER BY city_name, year