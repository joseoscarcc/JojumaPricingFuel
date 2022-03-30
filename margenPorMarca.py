from email import message_from_string
import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates

conn = sqlite3.connect('FuelPricing.sqlite')
CostoTADs = pd.read_sql_query("SELECT * FROM CostoTADs", conn)
MarcasPlaces = pd.read_sql_query("SELECT * FROM MarcasPlaces", conn)
conn.commit()
conn.close()

conn = sqlite3.connect('pricingGraphs.sqlite')
df = pd.read_sql_query("SELECT * FROM preciosSite", conn)
precios = df[df['date']=='02/21/2022']
conn.commit()
conn.close()

CostoTADs["precioXlitro"] = CostoTADs["precioXlitro"].apply(pd.to_numeric, errors='coerce')
CostoTADs['FECHADATE'] = pd.to_datetime(CostoTADs[['Year','Month','Day']])
mask = CostoTADs['FECHADATE'] == '2022-2-21'
CostoTADs = CostoTADs.loc[mask]

precios["place_id"] = precios["place_id"].apply(pd.to_numeric, errors='coerce')
MarcasPlaces["place_id"] = MarcasPlaces["place_id"].apply(pd.to_numeric, errors='coerce')

FuelSites = pd.merge(precios,MarcasPlaces,left_on='place_id',right_on='place_id')
FuelSites = FuelSites[FuelSites['EsNorte'] == "No"]

Marcas = ['OXXO GAS', 'CHEVRON', 'AKRON', 'CORPOGAS', 'ARCO', 'PEMEX', 'SHELL',
         'HIDROSINA','WINDSTAR','RENDICHICAS','BP','REPSOL','TOTAL','G500','MOBIL','GULF']

FuelSites = FuelSites[FuelSites['Marca'].isin(Marcas)]

terminalesTADS = pd.read_csv('rawData/terminalesMunicipios.csv')

def margen(price,estado,producto):
    terminal = terminalesTADS['TERMINAL'][terminalesTADS['ESTADO']==estado]
    costo = CostoTADs['precioXlitro'][(CostoTADs['PRODUCTO'] == producto) & (CostoTADs['REGIÓN'].isin(terminal))].mean()
    margin = ( price-costo)/1.16
    return margin

FuelSites['Margen'] = FuelSites.apply(lambda x: margen(x['prices'],x['Estado'],x['product']),axis=1)

TablaResults = FuelSites[['Marca','Estado','place_id','prices','product','Margen']].dropna()

RegularGraph = FuelSites[FuelSites['product'] == "regular"].pivot_table(values=['prices','Margen'], index='Marca', aggfunc=[np.mean])
RegularGraph.columns = RegularGraph.columns.droplevel(0)
PremiumGraph = FuelSites[FuelSites['product'] == "premium"].pivot_table(values=['prices','Margen'], index='Marca', aggfunc=[np.mean])
PremiumGraph.columns = PremiumGraph.columns.droplevel(0)
DieselGraph = FuelSites[FuelSites['product'] == "diesel"].pivot_table(values=['prices','Margen'], index='Marca', aggfunc=[np.mean])
DieselGraph.columns = DieselGraph.columns.droplevel(0)

#print(RegularGraph)

plt.figure()
plt.scatter(RegularGraph['Margen'],RegularGraph['prices'])
plt.ylabel('Precio por litro')
plt.xlabel("Margen por Litro")
plt.title('Margen y Precio promedio por Marca, Gasolina Regular al  21 feb 2022')
for index,row in RegularGraph.iterrows():
    plt.text(row[0]+.01,row[1],index,fontsize=8,color='green')
#plt.show()

plt.savefig('Reporte\AboutPageAssets\images\MxMReg.png')

plt.figure()
plt.scatter(PremiumGraph['Margen'],PremiumGraph['prices'])
plt.ylabel('Precio por litro')
plt.xlabel("Margen por Litro")
plt.title('Margen y Precio promedio por Marca, Gasolina Premium al  21 feb 2022')
for index,row in PremiumGraph.iterrows():
    plt.text(row[0]+.01,row[1],index,fontsize=8,color='orangered')
#plt.show()

plt.savefig('Reporte\AboutPageAssets\images\MxMPRE.png')

plt.figure()
plt.scatter(DieselGraph['Margen'],DieselGraph['prices'])
plt.ylabel('Precio por litro')
plt.xlabel("Margen por Litro")
plt.title('Margen y Precio promedio por Marca, Diesel al  21 feb 2022')
for index,row in DieselGraph.iterrows():
    plt.text(row[0]+.01,row[1],index,fontsize=8,color='black')
#plt.show()

plt.savefig('Reporte\AboutPageAssets\images\MxMDie.png')