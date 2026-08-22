-- Date
CREATE TABLE dim_date (
    date_key DATE PRIMARY KEY,
    year INT NOT NULL,
    month INT,
    month_name VARCHAR(20),
    quarter INT
);

-- City
CREATE TABLE dim_city (
    city_key SERIAL PRIMARY KEY,
    city_name VARCHAR(50) UNIQUE NOT NULL,
    province VARCHAR(50)
);

-- Housing Metrics
CREATE TABLE fact_housing_metrics (
    fact_id SERIAL PRIMARY KEY,
    city_key INT REFERENCES dim_city(city_key),
    date_key DATE REFERENCES dim_date(date_key),
    population BIGINT,
    avg_rent NUMERIC(10,2),
    vacancy_rate NUMERIC(5,2),
    interest_rate NUMERIC(5,2),
    num_units INT
);