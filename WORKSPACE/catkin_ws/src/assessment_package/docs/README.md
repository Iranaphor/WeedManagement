## Coordination:

Task: Spray all Weeds, while limiting the amount of spray on crops. Complete the task while controlling multiple Thorvald robots.  

This task was attempted by utilising distribution of tasks.  
Thorvald\_001: Identify weed locations.  
Thorvald\_002: Target and kill weeds.  

## Launch
`roslaunch assessment_package setup.launch`.  
`roslaunch assessment_package scanner_robot.launch`.  
`roslaunch assessment_package sprayer_robot.launch`.  

##Key Features
Coordination of multiple robots.
Detection against Basil, Cabbage and Onion.
Tranformation to /map frame.
system_config.yaml for easy configuration of many aspects.
Custom messages.
Custom sprayer system.
Many launch files for targeted management
Use of package.xml dependencies management
Heavilly Documentation


**See the docs folder for more information.**  
