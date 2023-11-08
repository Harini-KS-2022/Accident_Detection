import time
import cv2
import requests

import requests
import threading
import json
from flask import Flask, render_template, url_for, flash, redirect, Response, jsonify

from flask_bootstrap import Bootstrap

from detection import AccidentDetectionModel
import numpy as np
import os
from forms import LoginForm
global ip_address, lat, lon, query_result
model = AccidentDetectionModel("model.json", '123.h5')
font = cv2.FONT_HERSHEY_SIMPLEX
import pandas as pd
import math
import random
from twilio.rest import Client

account_sid = 'ACf7b90cb35e5c558d3cc4d90461996f17'
auth_token = 'ebbb3cadf341675cfbd4839db614c60e'


app = Flask(__name__)



app.secret_key = "akanksha"
Bootstrap(app)

l=[]

class Camera(object):

    def __init__(self):
        self.video = cv2.VideoCapture('cars6.mp4')
        self.accident_prob = 0


    def probability(self):

        while True:
            ret, frame = self.video.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            roi = cv2.resize(gray_frame, (250, 250))
            pred, prob = model.predict_accident(roi[np.newaxis, :, :])

            if pred == "Accident":
                prob = (round(prob[0][0] * 100, 2))
                if prob>=95:
                    l.append(prob)
                    break

        return l



    def startapplication(self):

        while True:
            ret, frame = self.video.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            roi = cv2.resize(gray_frame, (250, 250))

            pred, prob = model.predict_accident(roi[np.newaxis, :, :])
            if pred == "Accident":
                prob = (round(prob[0][0] * 100, 2))

                if prob>=99:
                    print("Alert Hospital")

                    print(prob)


            ret, jpg = cv2.imencode('.jpg', frame)
            return jpg.tobytes()


camera = Camera()


def gen():

    while True:
        frame = camera.startapplication()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.username.data == 'admin' and login_form.password.data == 'ab':
            return render_template('accident_page.html')

    return render_template('login.html', form=login_form)


@app.route('/accident_page')
def accident_page():

    return render_template('accident_page.html')


def detected():
    a = camera.probability()
    print(a)
    for prob in a:
        if prob >= 95:
            # time.sleep(5)
            return prob/100


@app.route('/accident_detected')
def accident_detected():

    i = random.randint(1, 2)
    if i == 1:
        response = requests.post("http://ip-api.com/batch", json=[
            {"query": "208.80.152.201"},
        ]).json()
    if i == 2:
        response = requests.post("http://ip-api.com/batch", json=[
            {"query": "208.81.123.202"},
        ]).json()

    for ipinfo in response:
        lat = ipinfo['lat']
        lon = ipinfo['lon']
        location = (lat, lon)
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f"Accident Detected. Latitude:{lat}, Longitude:{lon}. "
                 f"Please send ambulance and emergency services immediately.",
            from_="+15074769167",

            to="+918105138859 "

        )

        print(message.sid)
        radius = 10  # radius in kilometers
        nearby_hospitals_all = get_nearby_hospitals(location[0], location[1], radius)
        nearby_hospitals_all=nearby_hospitals_all[0:3]
        return render_template('accident_detected.html', ip_address_lat=lat,
                               ip_address_lon=lon, nearby_hospitals_all=nearby_hospitals_all)



@app.route('/get_accident_probability')
def get_accident_probability():
    accident_prob=detected()
    return jsonify(accident_prob=accident_prob)


hospitals_df = pd.read_csv('hospitals1.csv')


def distance(lat1, lon1, lat2, lon2):

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 111
    return c * r



def get_nearby_hospitals(latitude, longitude, radius):
    nearby_hospitals = []
    for index, row in hospitals_df.iterrows():
        hospital_latitude = row['LATITUDE']
        hospital_longitude = row['LONGITUDE']
        hospital_distance = distance(latitude, longitude, hospital_latitude, hospital_longitude)
        if hospital_distance <= radius:
            nearby_hospitals.append(row['NAME'])
    return nearby_hospitals


if __name__ == '__main__':

    app.run(debug=True)





