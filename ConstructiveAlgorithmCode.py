# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 15:26:40 2023

@author: DEMİRAY
"""

import time

from itertools import combinations,permutations
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







facilities = []

for i in range(len(cap)):
    facilities.append(Facility(str(i+1) , cap[i], False))
 
    
demand_points=[] 
for i in range(len(w)):
    demand_points.append(Demand_point(str(i+1) , w[i], distance[i], a[i]))


original_capacities = [facility.capacity for facility in facilities]
original_reinforcement_cap=capacity_of_reinforcement
array_of_selected_fac=[]

for i in range(P):
    best_obj_func_value=0
    best_fac=None
    for fac in facilities:
        min_distance = float("inf")
        closest_facility = None
        obj_func_value=0
        findingmax=[]
        sorted_dp = sorted(demand_points, key=lambda demand_point: demand_point.distances_to_facilities[int(fac.ID)-1])
        for dp in sorted_dp:
                distance = dp.distances_to_facilities[int(fac.ID) - 1]
                if fac.capacity >= dp.demand:
                    
                    
                        if dp.road_availability_to_facilities[int(fac.ID) - 1]:
                                
                            fac.capacity-=dp.demand
                            closest_facility = fac
                            findingmax.append(distance)
                            obj_func_value+=dp.demand
                        elif capacity_of_reinforcement >= distance:
                            fac.capacity-=dp.demand
                            closest_facility = fac
                            findingmax.append(distance)
                            obj_func_value+=dp.demand
    
        
                
        obj_func_value=obj_func_value-float(np.max(findingmax))*0.5
        if obj_func_value >= best_obj_func_value:
            best_obj_func_value = obj_func_value
            best_fac=fac
    array_of_selected_fac.append(best_fac)
    for fac in facilities:
        fac.capacity = original_capacities[int(fac.ID) - 1]
        capacity_of_reinforcement=original_reinforcement_cap
     
    facilities.remove(best_fac)

    
    
selected_assignment={}

max_distance_assigned=-1
max_distance_dp=None
max_distance_fac=None

road_statuses={}

objective_function_value=0

findingmax=[]
for dp in demand_points:
    closest_facility=None
    min_distance=float("inf")
    a=-1
    
    for fac in array_of_selected_fac:
        
            distance=dp.distances_to_facilities[int(fac.ID)-1]
        
            if distance<min_distance:
                
                if dp.road_availability_to_facilities[int(fac.ID)-1] and fac.capacity >= dp.demand:
                    
                    a=0
                    min_distance = distance
                    closest_facility = fac
                        
                elif capacity_of_reinforcement >= distance and fac.capacity >= dp.demand :
                    
                    a=1
                    min_distance = distance
                    closest_facility = fac
                        

    if closest_facility is not None and a==0:
        closest_facility.capacity -= dp.demand
        selected_assignment[dp.ID] = closest_facility.ID
        objective_function_value += dp.demand
        findingmax.append(min_distance)
    elif closest_facility is not None and a==1:
       
        capacity_of_reinforcement -= min_distance
        
        road_statuses[(dp.ID, closest_facility.ID)] = "Built"
        closest_facility.capacity -= dp.demand
        selected_assignment[dp.ID] = closest_facility.ID
        objective_function_value += dp.demand
        findingmax.append(min_distance)
    else:
        print(f"No suitable facility for demand point {dp.ID}")
for dp_id,fac_id in selected_assignment.items():
    print (f"The demand point {dp_id} is assigned to facility {fac_id}")
for (dp_id,fac_id),status in road_statuses.items():
    print(f"Road between demand point {dp_id} and facility {fac_id}: {status}")
    
    
for dp in sorted_dp:
    for fac in array_of_selected_fac:
        distance=max(findingmax)
        
        if dp.ID in selected_assignment and selected_assignment[dp.ID]==fac.ID and distance >max_distance_assigned and dp.distances_to_facilities[int(fac.ID)-1]==distance:
            max_distance_assigned=distance
            max_distance_dp=dp.ID
            max_distance_fac=fac.ID
            
print(f"Maximum distance used : {max_distance_assigned} between demand point {max_distance_dp} and facility {max_distance_fac}")

print(f"Objective funtion value:{objective_function_value}")

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

    

    
    
    
    