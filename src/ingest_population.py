import requests
import pandas as pd
import zipfile
import io
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Get the download link
product_id = "17100135"
link_url = f"https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{product_id}/en"
link_response = requests.get(link_url)
zip_url = link_response.json()["object"]
print(f"Download link: {zip_url}")

# Download the zip file
zip_response = requests.get(zip_url)
print(f"Downloaded {len(zip_response.content)} bytes")

# Unzip and read the CSV inside
with zipfile.ZipFile(io.BytesIO(zip_response.content)) as z:
    print("Files inside zip:", z.namelist())
    csv_filename = [f for f in z.namelist() if f.endswith(".csv")][0]
    with z.open(csv_filename) as f:
        df = pd.read_csv(f)

# Filter down 
cities_of_interest = [
    "Toronto (CMA), Ontario",
    "Montréal (CMA), Quebec",
    "Vancouver (CMA), British Columbia",
    "Calgary (CMA), Alberta",
    "Ottawa - Gatineau (CMA), Ontario/Quebec"
]

filtered = df[
    (df["GEO"].isin(cities_of_interest)) &
    (df["Sex"] == "Both sexes") &
    (df["Age group"] == "All ages")
]

print(df[df["GEO"].str.contains("Ottawa", na=False)]["GEO"].unique())

print(f"Filtered rows: {len(filtered)}")
print(filtered[["REF_DATE", "GEO", "VALUE"]].head(20))

filtered.to_csv(DATA_DIR / "population_raw.csv", index=False)
print("\nSaved population data!")