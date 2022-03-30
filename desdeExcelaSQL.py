import sqlite3
from datetime import date
import pandas as pd

conn = sqlite3.connect('FuelPricing.sqlite')
cur = conn.cursor()

tablaExcel = pd.read_csv('rawData/pemexTADS02-03.csv')

tablaExcel.to_sql('CostoTADs', conn, if_exists='append', index=False)
#print(precios.head())
conn.commit()
conn.close()

print(tablaExcel.head())
