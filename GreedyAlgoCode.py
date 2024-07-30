# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 23:02:57 2023

@author: DEMİRAY
"""
import time
from itertools import combinations
from datascience import*
import numpy as np
import pandas as pd
import ast

start_time = time.time()

class Facility:
    def __init__(self, ID, capacity,facility_opened_or_not):
        
        
        self.ID = ID
        self.capacity = capacity
        self.facility_opened_or_not=False

class Demand_point:
    def __init__(self, ID, demand, distances_to_facilities, road_availability_to_facilities):
        self.ID = ID
        self.demand = demand
        self.distances_to_facilities = distances_to_facilities
        self.road_availability_to_facilities = road_availability_to_facilities


excel_file = 'facility_data.xlsx'
df = pd.read_excel(excel_file, sheet_name='Sheet2')  # Assuming 'Sheet1' is the relevant sheet
df2=pd.read_excel(excel_file,sheet_name="Sheet1")




P = int(df.loc[0, 'P'])  
capacity_of_reinforcement = float(df.loc[0, 'DMAX'])
cap = [float(value) for value in df["faccap"]]
a = [ast.literal_eval(value) for value in df2["dptofacroad"]]
distance = [ast.literal_eval(value) for value in df2["dptofacdistance"]]
w = [float(value) for value in df2["dpdemand"]]
print(capacity_of_reinforcement)
facilities = []

for i in range(len(cap)):
    facilities.append(Facility(str(i+1) , cap[i], False))
 
    
demand_points=[] 
for i in range(len(w)):
    demand_points.append(Demand_point(str(i+1) , w[i], distance[i], a[i]))

sorted_facilities = []
for facility in facilities:
    sorted_facilities.append(facility)
    sorted_facilities.sort(key=lambda facility: facility.capacity, reverse=True)

opened_fac = []
for i in range(P):
    opened_fac.append(sorted_facilities[i])
    opened_fac[i].facility_opened_or_not=True

sorted_dp = []
for demand_point in demand_points:
    sorted_dp.append(demand_point)
    sorted_dp.sort(key=lambda demand_point: demand_point.demand, reverse=True)

selected_assignment={}

max_distance_assigned=-1
max_distance_dp=None
max_distance_fac=None

road_statuses={}

objective_function_value=0


for dp in sorted_dp:
    closest_facility=None
    min_distance=float("inf")
    a=0
    
    for fac in opened_fac:
        
            distance=dp.distances_to_facilities[int(fac.ID)-1]
        
            if distance<min_distance:
                
                if dp.road_availability_to_facilities[int(fac.ID)-1]:
                    if fac.capacity >= dp.demand:
                        a=0
                        min_distance = distance
                        closest_facility = fac
                elif capacity_of_reinforcement >= distance:
                    if fac.capacity >= dp.demand:
                        a=1
                        
                        min_distance = distance
                        closest_facility = fac
                        

    if closest_facility is not None and a==0:
       
        closest_facility.capacity -= dp.demand
        selected_assignment[dp.ID] = closest_facility.ID
        objective_function_value += dp.demand
    
    elif closest_facility is not None and a==1:
       
        capacity_of_reinforcement -= min_distance
        road_statuses[(dp.ID, closest_facility.ID)] = "Built"
        closest_facility.capacity -= dp.demand
        selected_assignment[dp.ID] = closest_facility.ID
        objective_function_value += dp.demand
    
    else:
        print(f"No suitable facility for demand point {dp.ID}")
for dp_id,fac_id in selected_assignment.items():
    print (f"The demand point {dp_id} is assigned to facility {fac_id}")
for (dp_id,fac_id),status in road_statuses.items():
    print(f"Road between demand point {dp_id} and facility {fac_id}: {status}")
    
    
for dp in sorted_dp:
    for fac in opened_fac:
        distance=dp.distances_to_facilities[int(fac.ID)-1]
        
        if dp.ID in selected_assignment and selected_assignment[dp.ID]==fac.ID and distance >max_distance_assigned:
            max_distance_assigned=distance
            max_distance_dp=dp.ID
            max_distance_fac=fac.ID
            
print(f"Maximum distance used : {max_distance_assigned} between demand point {max_distance_dp} and facility {max_distance_fac}")

print(f"Objective funtion value:{objective_function_value}")

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
