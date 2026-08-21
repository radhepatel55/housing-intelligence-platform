import requests
import pandas as pd
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Bank of Canada's interest rate
url = "https://www.bankofcanada.ca/valet/observations/V39079/json"

response = requests.get(url)
data = response.json()

observations = data["observations"]

# date + rate values table
rows = []
for obs in observations:
    date = obs["d"]
    rate = obs["V39079"]["v"]
    rows.append({"date": date, "interest_rate": rate})

df = pd.DataFrame(rows)
print(df.head())
print(f"\nTotal rows: {len(df)}")

df.to_csv(DATA_DIR / "interest_rates_raw.csv", index=False)
print("\nSaved raw interest rate data!")