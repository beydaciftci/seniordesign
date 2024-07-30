# -*- coding: utf-8 -*-
"""

Created on Mon Nov 13 14:45:00 2023

@author: DEMİRAY
"""
import xlsxwriter
import pandas as pd
import random

random.seed(2)

dpsize=70
facsize=30

dptofacroad=[[0]*facsize for _ in range(dpsize)]

for i in range(dpsize):
    for j in range(facsize):
        dptofacroad[i][j] = random.choice([0, 1])

print("a =" + str(dptofacroad))

dptofacdistance=[[0]*facsize for _ in range(dpsize)]

for i in range(dpsize):
    for j in range(facsize):
        dptofacdistance[i][j] = random.choice(range(7,30))
        
        
print("\n distance =" + str(dptofacdistance))        


dpdemand=[]
for i in range (dpsize):
    dpdemand.append(random.choice(range(30,100)))
    
print("\n w =" + str(dpdemand))    


faccap=[]

for i in range (facsize):
    faccap.append(random.choice(range(110,250)))
    
print("\n capacity =" + str(faccap))  


DMAX=random.choice(range(120,200))    

print("\n DMAX =" + str(DMAX))


P=random.choice(range(10,20)) 

print("\n P =" + str(P))

# Create an Excel writer
print(len(dptofacroad))
print(len(dptofacdistance))
print(len(dpdemand))
print(len(faccap))

df1 = pd.DataFrame({"dptofacroad": [row for row in dptofacroad],
                    "dptofacdistance": [row for row in dptofacdistance],
                    "dpdemand": dpdemand})

df2 = pd.DataFrame({"faccap": [random.choice(range(110, 250)) for _ in range(facsize)],
                    "DMAX": [DMAX] *facsize,
                    "P": [P] *facsize})

# Write to Excel
output_file = "facility_data.xlsx"

with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    df1.to_excel(writer, sheet_name='Sheet1', index=False)
    df2.to_excel(writer, sheet_name='Sheet2', index=False)

print(f"Data written to {output_file}")