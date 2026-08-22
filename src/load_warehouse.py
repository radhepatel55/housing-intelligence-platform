import pandas as pd
import psycopg2
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SILVER_DIR = SCRIPT_DIR.parent / "data" / "silver"

conn = psycopg2.connect(
    host="localhost", port=5432, dbname="housing_intelligence",
    user="postgres", password="housing123"
)
conn.autocommit = True
cursor = conn.cursor()

# Load the 5 unique city names
cities = ["Toronto", "Montreal", "Vancouver", "Calgary", "Ottawa"]
for city in cities:
    cursor.execute(
        "INSERT INTO dim_city (city_name) VALUES (%s) ON CONFLICT (city_name) DO NOTHING;",
        (city,)
    )
print(f"Loaded {len(cities)} cities into dim_city")

# Load one row per year (2001-2025)
for year in range(2001, 2026):
    date_key = f"{year}-01-01"
    cursor.execute(
        """INSERT INTO dim_date (date_key, year, month, month_name, quarter)
           VALUES (%s, %s, 1, 'January', 1) ON CONFLICT (date_key) DO NOTHING;""",
        (date_key, year)
    )
print("Loaded dim_date")


# Merge all 3 silver sources

population = pd.read_csv(SILVER_DIR / "silver_population.csv")
population = population.rename(columns={"year": "year"})[["city_name", "year", "population"]]

rental = pd.read_csv(SILVER_DIR / "silver_rental_market.csv")
rental_totals = rental[rental["unit_type"] == "Total"][["city_name", "survey_year", "average_rent_x" if False else "average_rent", "vacancy_rate_pct"]]
rental_totals = rental_totals.rename(columns={"survey_year": "year", "vacancy_rate_pct": "vacancy_rate"})

interest = pd.read_csv(SILVER_DIR / "silver_interest_rates.csv")
interest["year"] = pd.to_datetime(interest["date"]).dt.year
interest_yearly = interest.groupby("year")["interest_rate"].mean().reset_index()

# Merge population + rental on city_name + year 
merged = population.merge(rental_totals, on=["city_name", "year"], how="outer")

# Join interest rate by year
merged = merged.merge(interest_yearly, on="year", how="left")

print(merged.head(15))
print(f"\nTotal merged rows: {len(merged)}")

# Add to main table 
inserted = 0
skipped = 0

cursor.execute("TRUNCATE TABLE fact_housing_metrics;")
print("Cleared fact_housing_metrics for fresh load")
for _, row in merged.iterrows():
    if pd.isna(row["city_name"]):
        skipped += 1
        continue

    cursor.execute("SELECT city_key FROM dim_city WHERE city_name = %s;", (row["city_name"],))
    city_key_result = cursor.fetchone()

    date_key = f"{int(row['year'])}-01-01"

    if city_key_result:
        cursor.execute(
            """INSERT INTO fact_housing_metrics (city_key, date_key, population, avg_rent, vacancy_rate, interest_rate)
               VALUES (%s, %s, %s, %s, %s, %s);""",
            (city_key_result[0], date_key,
             None if pd.isna(row.get("population")) else int(row["population"]),
             None if pd.isna(row.get("average_rent")) else float(row["average_rent"]),
             None if pd.isna(row.get("vacancy_rate")) else float(row["vacancy_rate"]),
             None if pd.isna(row.get("interest_rate")) else float(row["interest_rate"]))
        )
        inserted += 1
    else:
        skipped += 1

print(f"\nInserted {inserted} rows into fact_housing_metrics, skipped {skipped}")


cursor.execute("""
    SELECT c.city_name, f.date_key, f.population, f.avg_rent, f.vacancy_rate, f.interest_rate
    FROM fact_housing_metrics f
    JOIN dim_city c ON f.city_key = c.city_key
    WHERE c.city_name = 'Toronto'
    ORDER BY f.date_key DESC
    LIMIT 5;
""")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
print("\nDimension tables loaded!")