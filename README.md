# Thorvald_Weed_Sprayer

---
## TODO:
:D - Swap out Thorvald_001 launch file names  
:| - Fix the sprayer alignment and spraying bugs  
:D - Rename the killbox  
Convert KILLER to CONFIG  
Write rest of readme.md  
:D - Copy movebase stuffs to assessment_package  
Test package.xml  
Remove unneccessary comments  
Rename Package  
:D - Remove extra .msg  
:D - Remove map folder  
:D - Comment /launch  
:D - Clean /launch  
Comment /scripts  
Clean /scripts  
Comment /config  
Clean /config  
:D - Comment /msg  
:D - Clean /msg  
Comment /scripts/image_processing  
Clean /scripts/image_processing  
:D - Custom sized XML objects  

---
## Coordination:

Task: Spray all Weeds, while limiting the amount of spray on crops. Complete the task while controlling multiple Thorvald robots.

This task was attempted by utilising distribution of tasks.

Thorvald\_001 was used to survey the crops for weeds.
Thorvald\_002 was used to target and spray the identified weeds.


#### Thorvald_001:
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

#### Setup.launch
> Single launch file to launch the system.
> #### Move_Base
> Used to offer simple-to-use movement systems to the Scanner and Sprayer robots.

> #### Scanner_Robot.launch
> > #### NAVIGATOR.launch
> > Responsible for moving thorvald_001 throughout the crop_rows, NAVIGATOR works its way through an array of crop rows defined by system_config

> > #### DETECTOR.launch
> > Based on the row published by NAVIGATOR this node runs image processing to extract the weeds, and transforms their coordinates in the image to world coordinates before sending them through to the Scanner

> #### Sprayer_Robot.launch
> > #### HUNTER.launch
> > Once the Scanner has moved through the first 2 rows, the hunter is given the coordinates of each weed in the region, it goes to each one in turn and calls the KILLER

> > #### KILLER.launch
> > Host to 2 spawnmodel services, this node works to spray the weeds when given the order

---
## Running the system

# 1.
> ``

# 2.
> ``

# 3.
> ``


---
## Known Issues

# Sprayer
> Occasionally the sprayer service call within **KILLER** does not work.
> ```Python
[ERROR] [1576073469.882153, 4537.860000]: bad callback: <bound method Killer.plot_point of <__main__.Killer instance at 0x7ff6d837bc20>>
Traceback (most recent call last):
  File "/opt/ros/kinetic/lib/python2.7/dist-packages/rospy/topics.py", line 750, in _invoke_callback
    cb(msg)
  File "/home/computing/Thorvald/WORKSPACE/catkin_ws/src/assessment_package/scripts/killer.py", line 125, in plot_point
    self.spawner(request)
  File "/opt/ros/kinetic/lib/python2.7/dist-packages/rospy/impl/tcpros_service.py", line 435, in __call__
    return self.call(*args, **kwds)
  File "/opt/ros/kinetic/lib/python2.7/dist-packages/rospy/impl/tcpros_service.py", line 525, in call
    raise ServiceException("transport error completing service call: %s"%(str(e)))
ServiceException: transport error completing service call: unable to receive data from sender, check sender's logs for details
```

---
