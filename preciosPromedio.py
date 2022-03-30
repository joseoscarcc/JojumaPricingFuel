from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

todays_date = date.today()

year = input("Enter year: ")
if len(year) < 1 : year = todays_date.year

month = input("Enter month: ")
if len(month) < 1 : month = todays_date.month

day = input("Enter day: ")
if len(day) < 1 : day = todays_date.day

fecha=month+"/"+day+"/"+year
fecha2018='11'+"/"+'30'+"/"+'2018'
# Create your connection.
conn = sqlite3.connect('pricingGraphs.sqlite')

df = pd.read_sql_query("SELECT * FROM preciosSite", conn)
precios = df[df['date']==fecha]
precios2018 = df[df['date']==fecha2018]

conn.commit()
conn.close()

conn = sqlite3.connect('FuelPricing.sqlite')

MarcasPlaces = pd.read_sql_query("SELECT * FROM MarcasPlaces", conn)
conn.commit()
conn.close()

precios["place_id"] = precios["place_id"].apply(pd.to_numeric, errors='coerce')
precios2018["place_id"] = precios2018["place_id"].apply(pd.to_numeric, errors='coerce')
MarcasPlaces["place_id"] = MarcasPlaces["place_id"].apply(pd.to_numeric, errors='coerce')

preciosMEX = pd.merge(precios,MarcasPlaces,left_on='place_id',right_on='place_id')
newDF = preciosMEX[preciosMEX['EsNorte'] == "Si"]
newDFTijuana = newDF[newDF['Municipio']=='Tijuana']
newDFMexicali = newDF[newDF['Municipio']=='Mexicali']
newDFNogales = newDF[newDF['Municipio']=='Nogales']
newDFJuarez = newDF[newDF['Municipio']=='Juárez']
newDFLaredo = newDF[newDF['Municipio']=='Nuevo Laredo']

newDF = preciosMEX[preciosMEX['EsNorte'] == "No"]

newDF2018 = pd.merge(precios2018,MarcasPlaces,left_on='place_id',right_on='place_id')
newDF2018 = newDF2018[newDF2018['EsNorte'] == "No"]

print('precios sin considerar los municipios fronterizos que tienen IVA al 8%')


#print(newDF.groupby('product').agg({'prices':np.average}))
print('Tijuana')
print(newDFTijuana.groupby('product').agg({'prices':np.average}))
print('Mexicali')
print(newDFMexicali.groupby('product').agg({'prices':np.average}))
print('Nogales')
print(newDFNogales.groupby('product').agg({'prices':np.average}))
print('Juarez')
print(newDFJuarez.groupby('product').agg({'prices':np.average}))
print('Nuevo Laredo')
print(newDFLaredo.groupby('product').agg({'prices':np.average}))
print('30 de noviembre de 2018')
print(newDF2018.groupby('product').agg({'prices':np.average}))
print('PROMEDIO NACIONAL HOY')
print(newDF.groupby('product').agg({'prices':np.average}))
