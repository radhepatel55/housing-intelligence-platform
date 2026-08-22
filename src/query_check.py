import psycopg2

conn = psycopg2.connect(
    host="localhost", port=5432, dbname="housing_intelligence",
    user="postgres", password="housing123"
)
cursor = conn.cursor()

cursor.execute("""
    SELECT city_name, year, population, population_growth_pct
    FROM public.mart_population_growth
    WHERE city_name = 'Toronto'
    ORDER BY year;
""")

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()