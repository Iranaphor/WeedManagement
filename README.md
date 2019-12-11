# Thorvald_Weed_Sprayer

---
## TODO:
:D - Swap out Thorvald_001 launch file names  
:( - Fix the sprayer alignment and spraying bugs  
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
Includes the following Files
> ##### Move_Base
> Initialise Navigation Stack
>
> ##### Scanner_Robot.launch
> > ##### NAVIGATOR.launch
> > Direct Scanner_Robot through a list of waypoints
> > ##### DETECTOR.launch
> > Runs image classification dependent on the row defined by NAVIGATOR
>
> ##### Sprayer_Robot.launch
> > ##### HUNTER.launch
> > Move to weed coordinates passed by detector, and call KILLER
> > ##### KILLER.launch
> > Host spawnmodel services, to spray weeds and mark simulation as required

---
## Running the system

# 1.
> ``

# 2.
> ``

# 3.
> ``


---
## Known System-Design Flaws

**Flaw:**  
The Sprayer Robot takes no penalty for driving over the crops to spray.  
**Possible soluition:**  
Restructure Hunter to drive down the centre of the row, drifting side to side to reach the targets.  
**Associated Files:**   
`scripts/hunter.py`  

**Flaw:**  
Lack of elegent management for Robot Locations.  
**Possible soluition:**  
Model the field as a topological map, and manage the robots using an system to lock edges in use, define a series of one-way systems, and setup a give-way policy for edge merging.  
**Associated Files:**  
`scripts/navigator.py`  
`scripts/hunter.py`  

**Flaw:**  
Translation issue between taking image, processing image and converting using tf.  
**Possible soluition:**  
The system currently makes use of the TransformPose function to move between the CameraFrame and the MapFrame. This can be replaced with use of `lookupTransform('map', 'robot_frame', t)`. The only element missing is a method to transform the pose along the same translation.   
**Associated Files:**  
`scripts/image_processing/camera_transformations.py`  

**Flaw:**  
Sprayer is not aligned properly.  
**Associated Files:**  
`scripts/hunter.py`    
`scripts/killer.py`  

**Flaw:**  
Weeds beyond region of camera are never picked up.  
**Associated Files:**  
`scripts/navigator.py`  
`scripts/detector.py`  

**Flaw:**  
Hunter plots points with no attempt to go to them.  
**Associated Files:**  
`scripts/hunter.py`    
`scripts/killer.py`  


---
## Known Issues

#### Sprayer
Occasionally the sprayer service call within `killer.py` does not work.  
``` python
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
