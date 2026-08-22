import psycopg2

conn = psycopg2.connect(
    host="localhost", port=5432, dbname="housing_intelligence",
    user="postgres", password="housing123"
)
cursor = conn.cursor()

cursor.execute("""
    SELECT city_name, year, population_growth_pct, housing_supply_growth_pct
    FROM public.mart_supply_vs_demand
    WHERE city_name = 'Toronto'
    ORDER BY year;
    """)

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()