WITH population_data AS (
    SELECT city_name, year, population,
           LAG(population) OVER (PARTITION BY city_name ORDER BY year) AS prev_population
    FROM {{ ref('stg_fact_housing') }}
    WHERE population IS NOT NULL
),

supply_data AS (
    SELECT
        city_name,
        survey_year AS year,
        num_units
    FROM {{ source('housing_raw', 'fact_housing_metrics') }} -- placeholder, will fix below
)

SELECT 1