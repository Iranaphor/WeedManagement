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

### Sprayer
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
### NAVIGATOR
When some of the waypoints are removed:
``` python
[ INFO:5] Initialize OpenCL runtime...
[ERROR] [1576149629.443096, 5000.600000]: bad callback: <bound method detector.row_type_callback of <__main__.detector instance at 0x7ff6d0d6a518>>
Traceback (most recent call last):
  File "/opt/ros/kinetic/lib/python2.7/dist-packages/rospy/topics.py", line 750, in _invoke_callback
    cb(msg)
  File "/home/computing/Thorvald/WORKSPACE/catkin_ws/src/assessment_package/scripts/detector.py", line 128, in row_type_callback
    self.cluster_data()
  File "/home/computing/Thorvald/WORKSPACE/catkin_ws/src/assessment_package/scripts/detector.py", line 147, in cluster_data
    self.plot_to_map((float(p[0]), float(p[1])), float(p[2]), 128)
  File "/home/computing/Thorvald/WORKSPACE/catkin_ws/src/assessment_package/scripts/detector.py", line 98, in plot_to_map
    self.weed_map = cv2.circle(self.weed_map, (center_coordinates[1],center_coordinates[0]), map_radius, gray, -1)
OverflowError: signed integer is greater than maximum
```
**Results:**
Observation still required, descaling of map has stopped the issue occuring.


### NAVIGATOR
Movement when config has basil rows removed skips first waypoint of cabbage (this may also be the case for basil but has gone unnoticed):
```
------------------------------
Moving to: -10, -4
tracker: 5612
row: home
(1)(1)(0:5593)(8)
(2)(0)(5612:5612)(8)
(2)(1)(5612:5612)(8)
(1)(1)(5612:5612)(8)
------------------------------
Moving to: 6.5, -0.75
row: cabbage
tracker: 5639
(1)(3)(5612:5612)(8)
(2)(1)(5639:5639)(7)
```
**Results:**
Observation still required, appending home point onto self.path seems to have resolved tyhe issue.


### SETUP.LAUNCH
Running scanner_robot.launch and sprayer_robot.launch within setup.launch doesnt work.
