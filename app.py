# Imports
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from datetime import datetime as now
from sqlalchemy import func

# Flask Application and Database Initialisation
app = Flask(__name__)
app.config["SECRET_KEY"] = "my-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy(app)


## Models ( Tables )
class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)

    def __init__(self, country, city):
        self.country = country
        self.city = city

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self.id


class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    sensor = db.relationship("Sensor")
    humidity = db.Column(db.Float, nullable=False)
    temp = db.Column(db.Float, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    def __init__(self, sensor_id, humidity, temp, wind_speed, datetime):
        self.sensor_id = sensor_id
        self.humidity = humidity
        self.temp = temp
        self.wind_speed = wind_speed
        self.datetime = datetime

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self.id


# Routes

# Sensor Registration Route
@app.route("/register", methods=["POST"])
def register():
    data = request.form
    try:
        country = data["country"]
        city = data["city"]

        sensor = Sensor(country, city)
        sensor_id = sensor.create()
        return {
            "sensor_id": sensor_id
        }, 201
    except:
        return {
            "error": "bad request"
        }, 400

# Sensor Data Update Route


@app.route("/update/<sensor_id>", methods=["POST"])
def upload(sensor_id):
    data = request.form
    try:
        humidity = data["humidity"]
        temp = data["temp"]
        wind_speed = data["wind_speed"]
        datetime = now.now()
        sensor = Sensor.query.filter_by(id=sensor_id).first()
        if not sensor:
            return {
                "error": "bad request"
            }, 400

        sensor = SensorData(sensor_id, humidity, temp, wind_speed, datetime)
        sensor_data_id = sensor.create()
        return {
            "sensor_id": sensor_data_id
        }, 201
    except Exception as e:
        print(e)
        return {
            "error": "bad request"
        }, 400


# Sensor Data Query Route
@app.route("/query", methods=["POST"])
def query():
    data = request.form
    try:
        sensors = data["sensors"]
        date_range = data["date_range"]
        metrics = data["metrics"]
        date = now.now() - timedelta(days=int(date_range))

        metrics = metrics.split(" ")

        if sensors == "all":
            sensors = [i.id for i in Sensor.query.all()]
        else:
            sensors = sensors.split(" ")

        result = {}

        for sensor in sensors:
            try:
                sensor_data = db.session.query(SensorData).filter(
                    SensorData.sensor_id == sensor).filter(SensorData.datetime > date)

                if not sensor_data:
                    return {
                        "error": "bad request"
                    }, 400
                
                
                count = sensor_data.count()

                response = {}

                if "humidity" in metrics:
                    humidity_sum = sensor_data.with_entities(func.sum(SensorData.humidity)
                                                             .label('total')).first().total
                    response["humidity"] = humidity_sum/count
                else:
                    humidity_sum = None

                if "temp" in metrics:
                    temp_sum = sensor_data.with_entities(func.sum(SensorData.temp)
                                                         .label('total')).first().total
                    response["temp"] = temp_sum/count
                else:
                    temp_sum = None

                if "wind_speed" in metrics:
                    wind_speed_sum = sensor_data.with_entities(func.sum(SensorData.wind_speed)
                                                               .label('total')).first().total
                    response["wind_speed"] = wind_speed_sum/count
                else:
                    wind_speed_sum = None

                result[sensor] = response

            except:
                continue

        return jsonify(result), 200

    except Exception as e:
        print(e)
        return {
            "error": "bad request"
        }, 400


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

"""
references : 
 1. https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.query.Query.with_entities.
 2. https://www.tutorialspoint.com/flask/flask_routing.htm
 3. https://stackoverflow.com/questions/3292752/sum-fields-in-sqlalchemy
"""


