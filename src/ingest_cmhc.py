import pandas as pd
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Source: https://www03.cmhc-schl.gc.ca/hmip-pimh/
cities_data = {
    "Calgary": {
        "vacancy_rate": {"Studio": [3.3, 0.7, 4.6, 6.0], "1 Bedroom": [2.9, 1.5, 4.6, 4.4],
                          "2 Bedroom": [2.6, 1.4, 5.1, 5.9], "3 Bedroom+": [2.8, 1.1, 3.7, 4.6],
                          "Total": [2.8, 1.4, 4.8, 5.1]},
        "average_rent": {"Studio": [975, 1207, 1363, 1442], "1 Bedroom": [1224, 1469, 1590, 1586],
                          "2 Bedroom": [1471, 1704, 1887, 1922], "3 Bedroom+": [1511, 1763, 1974, 2182],
                          "Total": [1337, 1577, 1735, 1764]},
        "num_units": {"Studio": [1624, 1792, 1908, 2044], "1 Bedroom": [22007, 23573, 25101, 27279],
                       "2 Bedroom": [20952, 22060, 24869, 27335], "3 Bedroom+": [1932, 1967, 2427, 3199],
                       "Total": [46515, 49392, 54305, 59857]},
    },
    "Montreal": {
        "vacancy_rate": {"Studio": [2.9, 2.2, 2.4, 3.6], "1 Bedroom": [1.9, 1.0, 1.8, 3.2],
                          "2 Bedroom": [2.4, 1.9, 1.3, 2.9], "3 Bedroom+": [None, None, None, 2.2],
                          "Total": [2.2, 1.6, 2.0, 3.0]},
        "average_rent": {"Studio": [790, 818, 901, 1014], "1 Bedroom": [909, 944, 1034, 1111],
                          "2 Bedroom": [994, 1046, 1127, 1349], "3 Bedroom+": [1235, 1324, 1547, 1693],
                          "Total": [972, 1036, 1135, 1272]},
        "num_units": {"Studio": [42491, 43090, 43397, 44786], "1 Bedroom": [118913, 120661, 122819, 126181],
                       "2 Bedroom": [224936, 226174, 230317, 229600], "3 Bedroom+": [44062, 44879, 45315, 45986],
                       "Total": [430402, 434804, 441848, 446553]},
    },
    "Vancouver": {
        "vacancy_rate": {"Studio": [1.2, 1.0, 1.9, 3.5], "1 Bedroom": [0.7, 0.6, 1.4, 2.6],
                          "2 Bedroom": [1.2, 1.2, 1.8, 2.4], "3 Bedroom+": [2.4, 1.3, 3.0, 2.2],
                          "Total": [0.9, 0.8, 1.6, 2.7]},
        "average_rent": {"Studio": [1419, 1529, 1618, 1705], "1 Bedroom": [1629, 1786, 1837, 1860],
                          "2 Bedroom": [2272, 2461, 2565, 2647], "3 Bedroom+": [3059, 2994, 3524, 3614],
                          "Total": [1726, 1884, 1967, 1994]},
        "num_units": {"Studio": [9563, 9935, 10158, 10664], "1 Bedroom": [40314, 41107, 41324, 41538],
                       "2 Bedroom": [11024, 11414, 11441, 11750], "3 Bedroom+": [791, 985, 1046, 1227],
                       "Total": [61692, 63441, 63969, 65179]},
    },
    "Toronto": {
        "vacancy_rate": {"Studio": [2.7, 1.7, 4.5, 4.2], "1 Bedroom": [1.9, 1.7, 2.7, 3.5],
                          "2 Bedroom": [1.3, 1.0, 1.7, 2.1], "3 Bedroom+": [1.1, 1.0, 1.4, 1.8],
                          "Total": [1.7, 1.4, 2.3, 2.8]},
        "average_rent": {"Studio": [1317, 1427, 1456, 1499], "1 Bedroom": [1538, 1708, 1715, 1763],
                          "2 Bedroom": [1811, 1992, 1985, 2055], "3 Bedroom+": [2096, 2241, 2268, 2361],
                          "Total": [1674, 1842, 1850, 1912]},
        "num_units": {"Studio": [23566, 23429, 23635, 24305], "1 Bedroom": [116236, 116426, 116973, 120040],
                       "2 Bedroom": [109090, 107898, 113903, 110563], "3 Bedroom+": [23436, 23228, 23348, 23893],
                       "Total": [272328, 270981, 277859, 278801]},
    },
    "Ottawa": {
        "vacancy_rate": {"Studio": [1.6, 1.6, 2.4, 3.5], "1 Bedroom": [2.0, 2.1, 2.4, 3.0],
                          "2 Bedroom": [2.3, 2.3, 2.8, 3.0], "3 Bedroom+": [2.5, 1.3, 1.7, 2.6],
                          "Total": [2.1, 2.1, 2.5, 3.0]},
        "average_rent": {"Studio": [1122, 1172, 1252, 1331], "1 Bedroom": [1348, 1415, 1526, 1597],
                          "2 Bedroom": [1633, 1713, 1896, 1926], "3 Bedroom+": [1947, 2118, 2191, 2203],
                          "Total": [1462, 1544, 1680, 1725]},
        "num_units": {"Studio": [5799, 6123, 6275, 6702], "1 Bedroom": [31340, 32092, 33341, 36455],
                       "2 Bedroom": [30285, 29543, 33624, 33061], "3 Bedroom+": [3044, 3031, 3164, 3647],
                       "Total": [70468, 70789, 76404, 79865]},
    },
}

# survey years
years = [2022, 2023, 2024, 2025]

rows = []
for city, metrics in cities_data.items():
    unit_types = metrics["vacancy_rate"].keys()
    for unit_type in unit_types:
        for i, year in enumerate(years):
            rows.append({
                "city": city,
                "unit_type": unit_type,
                "survey_year": year,
                "vacancy_rate_pct": metrics["vacancy_rate"][unit_type][i],
                "average_rent": metrics["average_rent"][unit_type][i],
                "num_units": metrics["num_units"][unit_type][i],
            })

df = pd.DataFrame(rows)
print(df.head(10))
print(f"\nTotal rows: {len(df)}")

df.to_csv(DATA_DIR / "cmhc_rental_market_raw.csv", index=False)
print("\nSaved CMHC rental market data!")