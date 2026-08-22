import psycopg2

conn = psycopg2.connect(
    host="localhost", port=5432, dbname="housing_intelligence",
    user="postgres", password="housing123"
)
conn.autocommit = True
cursor = conn.cursor()

cursor.execute("ALTER TABLE fact_housing_metrics ADD COLUMN IF NOT EXISTS num_units INT;")
print("Added num_units column")

cursor.close()
conn.close()