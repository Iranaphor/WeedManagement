## System Architecture

### Setup.launch
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
