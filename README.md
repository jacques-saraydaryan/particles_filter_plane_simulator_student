# Plane simulator for particule filter explanation

## Description
Base of program allowing to create particules to localise the plane

![Plane Simulator](https://github.com/jacques-saraydaryan/particules_filter_plane_simulator_student/blob/master/img/PlaneSimulator-v2.png "Application of particule filter for localising plane position")


## How to start

```
chmod +x ./scripts/Plane_Simulation.py
cd scripts
./Plane_Simulation.py

```

## Simulator command
* **Space bar**: pause resume the simulator
* **Left click**: Add an obstacle to the environment
* **Right click**: Remove an obstacle to the environment
* **S key**: Save the current environment (obstacles) into '\tmp\obstacles.npy'
* **R key**: Reset Plane position and particules filter
* **+ key**: Speed up the plane
* **- key**: Slow down the plane




## The job to do
Update the file Particule_Filter.py to:

1. Weight the particules


2. Select particules according the weights
3. Create new particules
```
def getRandParticule(self,nbr, start_x, max_x, start_y, max_y):
        particule_list = []
        ###################################
        ##### TODO
        ##   nbr: number fo particules
        ##   start_x: min x possible coordinate
        ##   max_x: max x possible coordinate
        ##   start_y: min y possible coordinate
        ##   max_y: max y possible coordinate
        #####
        ## Use the Particule object to fill the list particule_list
        ##

        return particule_list
```

4. Resample particules
