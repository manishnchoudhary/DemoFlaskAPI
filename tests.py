from numpy import record
from app import Sensor, SensorData, db
import datetime


def test_new_sensor():
    """
    GIVEN a Sensor model
    WHEN a new Sensor is created
    THEN check the metadata are defined correctly
    """
    sensor = Sensor('Ireland', 'Dublin')
    assert sensor.country == 'Ireland'
    assert sensor.city == 'Dublin'
    assert sensor.city != None


def test_new_sensor_data():
    """
    GIVEN a Sensor model
    WHEN a new Sensor is created
    GIVEN a SensorData model
    WHEN a new SensorData is created
    Then check if it is working properly
    """
    sensor = Sensor('Ireland', 'Dublin')
    record = SensorData(sensor.id, "95", "27", "1", datetime.datetime.now())
    assert record.sensor_id == None

    db.session.add(sensor)
    db.session.commit()

    record = SensorData(sensor.id, "95", "27", "1", datetime.datetime.now())
    assert record.sensor_id != None
