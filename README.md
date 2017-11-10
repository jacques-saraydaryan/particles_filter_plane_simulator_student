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
```
def weightingParticule(self,p_x, p_y, observed_distance):
        ###################################
        ##### TODO
        ##   p_x: x coordinate of the particule p
        ##  p_y: y coordinate of the particule p
        ##  observed_distance: distance to the ground
        ##  measure by the probe
        ##
        ## return weight corresponding to the given particule
        ## according observation
        ##
        ## Note ue the function distance_to_obstacle to get the
        ## estimate particule to the ground distance
        return ""
```

2. Select particules according the weights
```
def weighted_random_choice(self,choices):
        ###################################
        ##### TODO
        ##   choices: dictionary holding particule coordination as key
        ##  and weight as value
        ##  return the selected particule key
        #####
        return ""
```

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
```
def motion_prediction(self):
        new_particule_list = []
        choices = {}
        for i in range(len(self.particule_list)):
            choices[self.particule_list[i].id()] = self.particule_list[i].w

            ###################################
            ##### TODO
            ##   self.particule_list: list of available particules
            ##
            #####
            ## Use the function self.weighted_random_choice(choices) returning
            #  coordinate from a particule according a
            ##  roulette wheel algorithm
            #  Note that weighted_random_choice return a string containing coodinate x and y of the selected particule
            #   coord = self.weighted_random_choice(choices)
            #   x_coord = int(coord.split('_')[0])
            #   y_coord = int(coord.split('_')[1])

        return new_particule_list
```

## Example of result

[![Alt text](https://img.youtube.com/vi/3IBemFtwZ8g/0.jpg)](https://www.youtube.com/watch?v=3IBemFtwZ8g)
<div align="center">
    <iframe width="620" height="315"
        src="https://www.youtube.com/embed/3IBemFtwZ8g">
    </iframe>
</div>
