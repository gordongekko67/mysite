import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import  paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('altri', __name__, url_prefix='/altri')


def sendmsgMqtt():
    # inizialize MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("fkjqkoul", "wK0aUWpQWS35")
    client.connect("tailor.cloudmqtt.com", 16434, 60)
    client.subscribe("Tutorial2/#", 1)
    client.publish("Tutorial2", "avanti")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Tutorial2/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    if msg.payload.decode() == "prova":
        print("Robot avanti")


def on_publish(client, userdata, msg):
    print("Message published-> " + msg.topic + " " + str(msg.payload))  # Print a received msg


@bp.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method=='POST':
        titolo = request.form['titolo']
        autore = request.form['autore']
        inserisci_record(titolo,autore)
    return render_template('altri/scelta.html')

@bp.route('/scelta')
def scelta():
    session.clear()
    return render_template('altri/scelta.html')

@bp.route('/inserimento')
def inserim():
    session.clear()
    return render_template('altri/inserimento.html')

@bp.route('/chiamataREST', methods=['GET', 'POST'])
def chiamataREST():
    return "Chiamata REST"


@bp.route('/robotAvanti', methods=['GET', 'POST'])
def robotAvanti():
    if request.method == 'GET':
        sendmsgMqtt()
        return render_template('altri/scelta.html')



