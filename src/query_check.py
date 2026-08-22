import psycopg2

conn = psycopg2.connect(
    host="localhost", port=5432, dbname="housing_intelligence",
    user="postgres", password="housing123"
)
cursor = conn.cursor()

cursor.execute("""
    SELECT city_name, year, avg_rent, rent_growth_pct, affordability_rank
    FROM public.mart_city_affordability
    WHERE year = 2024
    ORDER BY affordability_rank;
""")

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()