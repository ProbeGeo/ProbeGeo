import pandas as pd
import os


if __name__ == "__main__":
    countries = pd.read_csv(os.path.join("..", "data", "countries_nominatim.csv"), encoding="utf-8")
    provinces = pd.read_csv(os.path.join("..", "data", "provinces_nominatim.csv"), encoding="utf-8")
    cities = pd.read_csv(os.path.join("..", "data", "cities_nominatim.csv"), encoding="utf-8")
    districts = pd.read_csv(os.path.join("..", "data", "districts_nominatim.csv"), encoding="utf-8")
    streets = pd.read_csv(os.path.join("..", "data", "streets_nominatim.csv"), encoding="utf-8")
    buildings = pd.read_csv(os.path.join("..", "data", "buildings_nominatim.csv"), encoding="utf-8")
    writer = pd.ExcelWriter(os.path.join("..", "data", "nominatim_location_distribution.xlsx"))
    countries.to_excel(writer, sheet_name='countries', index=False)
    provinces.to_excel(writer, sheet_name='provinces', index=False)
    cities.to_excel(writer, sheet_name='cities', index=False)
    districts.to_excel(writer, sheet_name='districts', index=False)
    streets.to_excel(writer, sheet_name='streets', index=False)
    buildings.to_excel(writer, sheet_name='buildings', index=False)
    writer.save()
    writer.close()