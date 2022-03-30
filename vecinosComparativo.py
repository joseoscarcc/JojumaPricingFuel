from cProfile import label
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from math import cos, sqrt, pi
import gmplot

producto = 'regular'
encuentraPlaceID = 6432


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


conn.commit()
conn.close()

conn = sqlite3.connect('FuelPricing.sqlite')

MarcasPlaces = pd.read_sql_query("SELECT * FROM MarcasPlaces", conn)
conn.commit()
conn.close()

precios["place_id"] = precios["place_id"].apply(pd.to_numeric, errors='coerce')
MarcasPlaces["place_id"] = MarcasPlaces["place_id"].apply(pd.to_numeric, errors='coerce')

preciosMEX = pd.merge(precios,MarcasPlaces,left_on='place_id',right_on='place_id')

site = preciosMEX[preciosMEX['place_id']==encuentraPlaceID]
site = site[site['product']==producto]
municipio = site['Municipio']
estado = site['Estado']
for key, value in site['x'].items():
    xsite = value
for key, value in site['y'].items():
    ysite = value

comparativo=preciosMEX[preciosMEX['Estado'].isin(estado)]
comparativo=comparativo[comparativo['Municipio'].isin(municipio)]
comparativo=comparativo[comparativo['product']==producto]

R = 6371000 #radius of the Earth in m 
def distance(lon1, lat1, lon2, lat2): 
    x = (lon2 - lon1) * cos(0.5*(lat2+lat1))
    y = (lat2 - lat1)
    return (2*pi*R/360) * sqrt( x*x + y*y )

comparativo['distancia'] = comparativo.apply(lambda x: distance(x.x,x.y,xsite,ysite),axis=1)

mascercanos = comparativo.sort_values(by='distancia')

masceranos = mascercanos[['place_id','prices','cre_id','Marca','distancia','x','y']]
df =masceranos.head(10)

apikey='AIzaSyA92fyf7foR--PyViIHgyC-bhXNYLtZOF8'
gmap3 = gmplot.GoogleMapPlotter(ysite, xsite, 13, apikey=apikey)
  
# scatter method of map object 
# scatter points on the google map
gmap3.scatter( df.y, df.x, 'red', size = 40, marker = True)
print(df.Marca)
gmap3.draw( "mapa.html" )

print(df)


