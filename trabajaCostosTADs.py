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

conn.commit()
conn.close()
print(CostoTADs.info())

CostoTADs["precioXlitro"] = CostoTADs["precioXlitro"].apply(pd.to_numeric, errors='coerce')

CostoTADs['FECHADATE'] = pd.to_datetime(CostoTADs[['Year','Month','Day']])
CostoTADs['WeekDay'] = CostoTADs['FECHADATE'].dt.dayofweek


CostoTADs = CostoTADs[CostoTADs['REGIÓN']=='CADEREYTA']
mask = (CostoTADs['FECHADATE'] > '2018-11-30') & (CostoTADs['FECHADATE'] <= '2022-2-21')

#CostoTADs['COSTO'] = CostoTADs['COSTO']/1000
CostoTADs = CostoTADs.loc[mask]
#CostoTADs = CostoTADs.set_index('FECHADATE')
newCosto = CostoTADs.pivot_table(values='precioXlitro', index='FECHADATE',columns='PRODUCTO', aggfunc=[np.mean])
newCosto.columns = newCosto.columns.droplevel(0)

print(newCosto.head())
# plot
plt.plot(newCosto['Regular'], 'b-', c='green')
plt.plot(newCosto['Premium'], 'b-', c='red')
plt.plot(newCosto['Diesel'], 'b-', c='black')


plt.xlabel('Año - Mes')
plt.ylabel("Costo en MXN x Litro")
plt.title('Variación del costo en terminal PEMEX "CADEREYTA"')
plt.legend(['Regular','Premium','Diesel'], loc=0, frameon=False)

x = plt.gca().xaxis

# rotate the tick labels for the x axis
for item in x.get_ticklabels():
    item.set_rotation(45)

plt.subplots_adjust(bottom=0.25)
plt.axhline(17.61, color='blue',ls='--', zorder=1)
plt.text(date(2021, 3, 5), 17,'*Costo el 30-11-2018')

# Create rectangle x coordinates
startTime = date(2020, 2, 15)
endTime = date(2020, 6, 30)

# convert to matplotlib date representation
start = mdates.date2num(startTime)
end = mdates.date2num(endTime)
width = end - start

# Plot rectangle
rect = Rectangle((start, 12), width, 4, color='yellow')
plt.gca().add_patch(rect)
plt.text(date(2020, 7, 5), 12.4,'*Efecto del inicio de la pandemia', color='orangered')

#plt.show()

plt.savefig('Reporte\AboutPageAssets\images\Terminal03.png')



