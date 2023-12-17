# This is the backend assignment of EnviewAI.

## Project Description

`EnviewAI` is building a driver monitoring solution. Our customer has a fleet of delivery vehicles. They have had problems where drivers drive rashly or use their phones while driving, leading to accidents. We have built a model that detects this behavior. We have deployed the model in an IoT device on the vehicle. Every minute, the model emits a driving event with two fields:
 - `timestamp` of type ISO date time 
 - `is_driving_safe` of type boolean. 
 - `vehicle_id` a unique ID associated with a vehicle
 - `location_type` one of the following values: `highway` , `residential` , `commercial` , `city_center` .


**The Rule Engine**
Our customer wants to know if the driver is not driving safely. However, they don’t want to get
alerted every time this happens- they are only interested in repeated speed violations.
Further, a speed violation in a residential area is more serious than a speed violation on a highway.
It’s dangerous to drive over 60kmph in a residential area, but not so much on a highway.
Therefore, we have a rule engine that aggregates and transforms driving events into alerts that will
be shown to the customer. 
## Requirements

- Python = `3.8`
- Flask
- requests

## Installation & Reproducing Result

- Make a python virtual environment. `python -m venv venv ` or use ` conda create -p virtual_env_name python == 3.8 ` (preferred).
- Install the project and put in your root directory. At the end your root directory should have app, database, etc.
- Run ` python database/database.py `
- Run ` python app/app.py `
- Run ` python iot_simulator.py ` 
