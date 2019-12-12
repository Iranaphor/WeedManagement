## Coordination:

Task: Spray all Weeds, while limiting the amount of spray on crops. Complete the task while controlling multiple Thorvald robots.

This task was attempted by utilising distribution of tasks.

Thorvald\_001 was used to scan the crops for weeds.
Thorvald\_002 was used to target and spray the identified weeds.


### Thorvald_001:
Thorvald\_001 is started using `roslaunch assessment_package weed_detector.launch`
This runs the script `navigator.py`, and 2 copies of `weed_detector.py`.

### Navigator.py
This script reads a path from `/config/navigation_targets.yaml`.
This path is then passed to movebase to ensure the robot covers all of the crop paths.

### Weed_Detector.py
This script takes the arguments (`robot_name`, `plant_type`) ...etc
It is used to run individual scripts to identify weeds against the crops
