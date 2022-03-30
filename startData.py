import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3


#fruits = pd.read_table('readonly/fruit_data_with_colors.txt')
IEPS=pd.read_csv('IEPS.csv')
#print(IEPS.head())

ClusterDescuentos=pd.read_csv('clusterDescuentos.csv')
#print(ClusterDescuentos.head())

CostoTADs = pd.read_csv('CostoTADs.csv')
#print(CostoTADs.head())

DescuentosProveedores=pd.read_csv('DescuentosProveedores.csv')
#print(DescuentosProveedores.head())

proveedores=pd.read_csv('proveedores.csv')
#print(proveedores.head())

ReporteCostos=pd.read_csv('ReporteCostos.csv')
#print(ReporteCostos.head())

conn = sqlite3.connect('FuelPricing.sqlite')
cur = conn.cursor()

IEPS.to_sql('IEPS', conn, if_exists='replace', index=False) # - writes the pd.df to SQLIte DB
ClusterDescuentos.to_sql('ClusterDescuentos', conn, if_exists='replace', index=False)
CostoTADs.to_sql('CostoTADs', conn, if_exists='replace', index=False)
DescuentosProveedores.to_sql('DescuentosProveedores', conn, if_exists='replace', index=False)
proveedores.to_sql('proveedores', conn, if_exists='replace', index=False)

conn.commit()
conn.close()
