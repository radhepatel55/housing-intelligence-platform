SELECT
    f.fact_id,
    c.city_name,
    d.year,
    f.population,
    f.avg_rent,
    f.vacancy_rate,
    f.interest_rate
FROM {{ source('housing_raw', 'fact_housing_metrics') }} f
JOIN {{ source('housing_raw', 'dim_city') }} c ON f.city_key = c.city_key
JOIN {{ source('housing_raw', 'dim_date') }} d ON f.date_key = d.date_key