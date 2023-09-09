from flask import Flask, render_template
from flask_mqtt import Mqtt
import random
import time
import datetime
import pytz

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  
app.config['MQTT_PASSWORD'] = ''  
app.config['MQTT_KEEPALIVE'] = 60  
app.config['MQTT_TLS_ENABLED'] = False  
topic = 'RedPanda/LalBus'

mqtt_client = Mqtt(app)

TRACKER_1_DID = "1043002210110001"
TRACKER_2_DID = "1043002210110002"
#total_data,valid_data,started,disconnected,date
tracker_data_1 = [0,0,0,"0"]
tracker_data_2 = [0,0,0,"0"]

dhaka_timezone = pytz.timezone('Asia/Dhaka')

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print('Received message on topic: {topic} with payload: {payload}'.format(**data))
    payload = message.payload.decode("utf-8")
    print("Received message: " + payload)
    global tracker_data_1 , tracker_data_2
    try:
            data = payload.split(',')
            if (data[0] == TRACKER_1_DID):
                #total_data,started,disconnected,date
                if (data[1] == "started"):
                    tracker_data_1[1] = tracker_data_1[1]+1
                elif (data[1] == "mqtt_disconnected"):
                    tracker_data_1[2] = tracker_data_1[2]+1
                else:
                    tracker_data_1[0] = tracker_data_1[0]+1
            elif (data[0] == TRACKER_2_DID):
                if (data[1] == "started"):
                    tracker_data_2[1] = tracker_data_2[1]+1
                elif (data[1] == "mqtt_disconnected"):
                    tracker_data_2[2] = tracker_data_2[2]+1
                else:
                    tracker_data_2[0] = tracker_data_2[0]+1

    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")

@app.route('/publish', methods=['POST'])
def publish_message():
   request_data = request.get_json()
   publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
   return jsonify({'code': publish_result[0]})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_tracker_data_1')
def get_tracker_1():
    global tracker_data_1 #total_data,started,disconnected,date
    tracker_total_data = tracker_data_1[0]
    tracker_total_started = tracker_data_1[1]
    tracker_total_mqtt_disconnected = tracker_data_1[2]
    tracker_last_online = datetime.datetime.now(dhaka_timezone)

    tracker_data_1 = [tracker_total_data, tracker_total_started, tracker_total_mqtt_disconnected,tracker_last_online]
    return {'tracker_data_1': tracker_data_1}

@app.route('/get_tracker_data_2')
def get_tracker_2():
    global tracker_data_2
    tracker_total_data = tracker_data_2[0]
    tracker_total_started = tracker_data_2[1]
    tracker_total_mqtt_disconnected = tracker_data_2[2]
    tracker_last_online = datetime.datetime.now(dhaka_timezone)

    tracker_data_2 = [tracker_total_data, tracker_total_started, tracker_total_mqtt_disconnected,tracker_last_online]
    return {'tracker_data_2': tracker_data_2}

'''
Tracker:
 DID
 Total Data:
 Total Valid Data:
 Total Start:
 Total Mqtt Disconnected: 
 Last Online:

Tracker:
 DID
 Total Data:
 Total Valid Data:
 Total Master Start:
 Total Slave Start:
 Total Mqtt Disconnected: 
 Last Online:

'''


if __name__ == '__main__':
   app.run(host='127.0.0.1', port=5000)