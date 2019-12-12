## Running the system

### 1. Download the src folder to a catkin workspace

### 2. CD to the folder holding the src
``` bash
cd ${path_to_clone}
```

### 3. Download and install the dependencies
``` bash
rosdep install --from-paths . -i -y
```

### 4. Build the catkin_workspace
``` bash
catkin_make
```

### 5. Source the workspace
``` bash
source ./devel/setup.bash
```

### 6. Modify the Config file as required
'''
roscd assessment_package/config
gedit ./system_config.yaml
'''

### 7. Launch the setup.launch
``` bash
roslaunch assessment_package setup.launch
```

### 8. Launch the scanner_robot
``` bash
roslaunch assessment_package scanner_robot.launch
```

### 9. Launch the sprayer_robot
``` bash
roslaunch assessment_package sprayer_robot.launch
```

### 10. (optional) View the Scanner output
``` bash
rosrun image_view image_view image:=thorvald_001/DETECTOR/OVERLAY
```
