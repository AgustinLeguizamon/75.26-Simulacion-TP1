# 75.26-Simulacion-TP1

## Ejercicio 5

### Celullar automata

Parts:
* cells
* cell space
* neighbors
* rule

#### Simulates 

##### crosswalk
Fixed **pedestrian signal** time of 90s
    6 green classes = 25, 30, 35, 40, 45, 50s green time
    6 red classes = 65, 60, 55, 50, 45, 40s red time

Width
    6 width classes = 2.5, 3, 3.5, 4 , 4.5, 5m

Crossing Length
    21 m

Divided in **cells**
    square size: 0.5 x 0.5 m2
    states: empty or one pedestrian

##### Pedestrian
Initial velocity
    classes = 2, 3 ,4 ,5 ,6 cells/second
    1 m/s -> 2 cells/s

Updates velocity at each step

##### Vehicles
Size = 6 x 5 cells
veolcity = 5 m/s -> 10 cells/s
    

##### Pedestrian waiting areas
both side of crosswalk
can hold up to 100 **pedestrians**

##### Road segment
two-way six-vehicle lanes
Each lane
    Width: 3.5 mts

##### boundary condition
Open boundary condition: certain probability when a vehicle is inserted 
and removed from the boundary cell, translational invariance is broken but one can still expect stationary states
with non trivial density profile.

#### Evolution rules
Three basic laws
lateral movement: path change behaviour, obtain acceleration space and avoid head-on collision


linear movement: personal preference + neighbors = velocity (cells/s)

collision avoidance: how to avoid collision for pedestrians, walking close to each other
along the opossite direction

##### Pedestrian rules

1. Arrival of pedestrian
Poisson dsitribution lambdaP
2. Pedestrian give priority to front cell as their destination
Cab move forward v (actual speed) cells or change left o right when blocked 
2.a Step forward: initial velocty assigned with probabilities
[0.273, 0.52, 0.137, 0.0480, 0.0220] (es la misma proba acumulada que el ejercicio 2)

vi,j = velocity pedestrian in grid (i, j)

Velocty update
Vi,j = min {di,j, v,i,h}

di,j: distance to nearest vertically fron pedestrian (i = 0 p1 - - - p2 entonces d0j = 3)

2.b Lane change: if any condition is satisfied, **lane change** happends
(3.4) left or right
(3.5) right
(3.6) left

(3.4) si tiene uno adelante && a la derecha y a la ziquierda esta vacio && la distancia 
al vecino lateral mas cercan es mayor a su velocidad actual && 'velocidad de los primeros vecinos laterales 
que estan n celdas mas atras' es menor a su velocidad actual

xi,j = denotes location of pedestrian (booleano?)

j

|-|x|-|
|-|X|-|-|-|x|
|-|-|-|
|x|-|x|



3. If two compete for one, randomly selected, the other stays in cell
4. Wait red light, unless not finished crossing when green light ends. 
Accelerate to maximum velocity if green light end
5. Opposite pedestrians. Can span(cruzarse/intercambiar) each other if destination cell is empty
otherwise, adjust velocity or keep original position

##### Vehicle Rules

1. Poisson with arrival Lambdav
2. if **pedestrian signal** red and no pedestrians in crosswalk, vehicles cross. Otherwise, conflict

##### Conflicts rules between Pedestrian adn Vehicle
Classified as 4 areas

2 conflict-related definitions
1. Pedestrian vehicle
   Order to avoid collision, vehicle stops moving forward into cells currently occupied 
by at least one pedestrian or will be occupied

2. Pedestrian conflic delay
    pedestrian waits to avoid passing-through vehicles when conflict happens

Conflict rules
1. Pedestrian target cell ocuppied by vehicle, vehicle has priority and viceversa
2. If overlap target cell, priorty random equal probability 

#### Simulation results
MATLAB
Span for each step is 1 second
data recorded every 3600 time steps
30 simulations - average as result analyses