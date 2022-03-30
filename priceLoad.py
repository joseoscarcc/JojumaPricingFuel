import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import xml.etree.ElementTree as ET
from datetime import date
import ssl
import sys
import pandas as pd

conn = sqlite3.connect('pricingGraphs.sqlite')
cur = conn.cursor()

precios = pd.DataFrame()
todays_date = date.today()

year = input("Enter year: ")
if len(year) < 1 : year = todays_date.year

month = input("Enter month: ")
if len(month) < 1 : month = todays_date.month

day = input("Enter day: ")
if len(day) < 1 : day = todays_date.day

fecha=month+"/"+day+"/"+year

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url='https://publicacionexterna.azurewebsites.net/publicaciones/prices'
print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)



data = uh.read()
tree = ET.fromstring(data)


#tree = ET.parse('rawData/20210222-preciosCRE.xml')

places = tree.findall('place')

for place in places:
    place_id = place.get('place_id')
    prices = place.findall('gas_price')
    for price in prices:
        product = price.get('type')
        elPrecio = float(price.text)
        elDict ={ 'place_id' : place_id, 'prices': elPrecio, 'product': product, 'date' : fecha}
        temp = pd.DataFrame([elDict])
        precios = pd.concat([precios,temp])

precios.to_sql('preciosSite', conn, if_exists='append', index=False)
#print(precios.head())
conn.commit()
conn.close()
