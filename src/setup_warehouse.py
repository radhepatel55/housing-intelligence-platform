import psycopg2
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SQL_DIR = SCRIPT_DIR.parent / "sql"

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="housing_intelligence",
    user="postgres",
    password="housing123"
)
conn.autocommit = True
cursor = conn.cursor()

# Run SQL file
with open(SQL_DIR / "create_schema.sql", "r") as f:
    schema_sql = f.read()

cursor.execute(schema_sql)
print("Schema created successfully!")

# Verify
cursor.execute("""
    SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'public';
""")
tables = cursor.fetchall()
print("Tables in database:", [t[0] for t in tables])

cursor.close()
conn.close()