import pandas as pd
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data" / "raw"
SILVER_DIR = SCRIPT_DIR.parent / "data" / "silver"
SILVER_DIR.mkdir(parents=True, exist_ok=True)

# --- Interest rates (national, no city needed) ---
interest_rates = pd.read_csv(DATA_DIR / "interest_rates_raw.csv")
interest_rates["date"] = pd.to_datetime(interest_rates["date"])
interest_rates.to_csv(SILVER_DIR / "silver_interest_rates.csv", index=False)
print(f"Interest rates: {len(interest_rates)} rows")

# --- CMHC rental data: already uses simple city names, just standardize the column name ---
cmhc = pd.read_csv(DATA_DIR / "cmhc_rental_market_raw.csv")
cmhc = cmhc.rename(columns={"city": "city_name"})
cmhc.to_csv(SILVER_DIR / "silver_rental_market.csv", index=False)
print(f"CMHC rental: {len(cmhc)} rows, cities: {cmhc['city_name'].unique()}")

# --- StatCan population: standardize the long CMA names down to simple city names ---
population = pd.read_csv(DATA_DIR / "population_raw.csv")

geo_to_city = {
    "Toronto (CMA), Ontario": "Toronto",
    "Montréal (CMA), Quebec": "Montreal",
    "Vancouver (CMA), British Columbia": "Vancouver",
    "Calgary (CMA), Alberta": "Calgary",
    "Ottawa - Gatineau (CMA), Ontario/Quebec": "Ottawa",
}

population["city_name"] = population["GEO"].map(geo_to_city)
population = population.rename(columns={"REF_DATE": "year", "VALUE": "population"})
population = population[["city_name", "year", "population"]]

population.to_csv(SILVER_DIR / "silver_population.csv", index=False)
print(f"Population: {len(population)} rows, cities: {population['city_name'].unique()}")