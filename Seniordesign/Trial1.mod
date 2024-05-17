/*********************************************
 * OPL 22.1.0.0 Model
 * Author: Group6
 * Creation Date: May 1, 2023 at 4:41:19 PM
 *********************************************/

 //Indicies
 int dem_points=...; range DP=1..dem_points;
 int candfacility_points=...; range CF=1..candfacility_points;
 // Parameters
 float distance[DP][CF]=...;
 int capacity[CF]=...;
 int P=27;
 int DMAX =184 ;
 int w[DP]=...;
 int a[DP][CF]=...;
 float epsilon=0.5 ;
 // Decision Variables
 dvar boolean Y[DP][CF];
 dvar boolean X[CF];
 dvar boolean Z[DP][CF];
 dvar float+ DbMax;
 execute
{
  cplex.tilim=1800; // 30 dk  time limt
   
}
 //Objective Function
 dexpr int totaldemand= sum(i in DP, j in CF) w[i] * Y[i][j]; 
 dexpr float MaximumDistanceCovered =  epsilon *DbMax;
 dexpr float objective = totaldemand -  MaximumDistanceCovered; 
 maximize objective ;
 
// Constraints
subject to {
  // Locate P facilities
  sum(j in CF) X[j] == P; 
  // Ensure each location is served 
  forall(i in DP)
    sum(j in CF) Y[i][j] <= 1;
  // Ensure operating facilities have enough capacity 
  forall(j in CF)
    sum(i in DP) w[i] * Y[i][j] <= capacity[j] * X[j];
    //picking the maximum distance for serving 
    forall(i in DP, j in CF)
      distance[i][j] * Y[i][j] <= DbMax;
  // ensure that there exists a route from operating facility location 
   forall(i in DP, j in CF)
 Y[i][j]  <= a[i][j] + Z[i][j] ; 
    //to start construction if route is damaged
forall(i in DP, j in CF)
	Z[i][j] - (1-a[i][j])*X[j]<= 0; 
  // Max distance that can be reinforced 
sum(i in DP, j in CF) distance[i][j] * Z[i][j]  <=DMAX;
}

