# Thorvald_Weed_Sprayer

## Coordination:

Task: Spray all Weeds, while limiting the amount of spray on crops. Complete the task while controlling multiple Thorvald robots.

This task was attempted by utilising distribution of tasks.

Thorvald\_001 was used to survey the crops for weeds.
Thorvald\_002 was used to target and spray the identified weeds.


### Thorvald_001:
Thorvald\_001 is started using `roslaunch assessment_package weed_detector.launch`
This runs the script `navigator.py`, and 2 copies of `weed_detector.py`.

#### Navigator.py
This script reads a path from `/config/navigation_targets.yaml`.
This path is then passed to movebase to ensure the robot covers all of the crop paths.

#### Weed_Detector.py
This script takes the arguments (`robot_name`, `plant_type`) ...etc
It is used to run individual scripts to identify weeds against the crops


---
## System Architecture

# Setup.launch
> # Move_Base
> - Used to offer simple-to-use movement systems to the Scanner and Sprayer robots.
> # Thorvald_001.launch
> - Used to Manage the Scanner Robot and its 2 core processes.
> > # NAVIGATOR.launch
> > - Responsible for moving thorvald_001 throughout the crop_rows, NAVIGATOR works its way through an array of crop rows defined by system_config
> > # DETECTOR.launch
> > - Based on the row published by **NAVIGATOR** this node runs image processing to extract the weeds, and transforms their coordinates in the image to world coordinates before sending them through to the Scanner
> # Thorvald_002.launch
> - Used to Manage the Sprayer Robot and its 2 core processes.
> > # HUNTER.launch
> > - Once the Scanner has moved through the first 2 rows, the hunter is given the coordinates of each weed in the region, it goes to each one in turn and calls the **KILLER**
> > # KILLER.launch
> > - Host to 2 spawnmodel services, this node works to spray the weeds when given the order

---
## Running the system

# 1. 
> ``

# 2. 
> ``

# 3. 
> ``


---



