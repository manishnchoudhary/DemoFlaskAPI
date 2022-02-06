# Weather_Rest_API 

**app.py**

The sensor table collects different sensors id, countries and cities at one time in the table. Sensors update their humidity, temperature, wind_speed and data time in the SensorData table.

### 3 methods developed for this rest api.

**1- register method -** This method is used for registering sensor id, country and city.
127.0.0.1:5000/register

**2- update -** This method is used for registering senor_id, humidity, temp(temperature), wind_speed(wind speed) and DateTime(current date-time of sensor's data)
127.0.0.1:5000/update/<sensor_id>

**3- query -** This method is used for filtering data from stored information. Filtering parameters are sensors (sensor_id: eg.  1,2,3,4 etc), data_range(1,2,3..etc)
127.0.0.1:5000/query


**tests.py**

It is a python file for automated testing.


## Entity Digram

![App Screenshot](https://github.com/manishnchoudhary/DemoFlaskAPI/blob/main/ER_Digram.png)


**References :** 
 1. https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.query.Query.with_entities.
 2. https://www.tutorialspoint.com/flask/flask_routing.htm
 3. https://stackoverflow.com/questions/3292752/sum-fields-in-sqlalchemy


## Demo

**Querying**

I have used Postman tool. 

![App Screenshot](https://github.com/manishnchoudhary/DemoFlaskAPI/blob/main/Query.png)





