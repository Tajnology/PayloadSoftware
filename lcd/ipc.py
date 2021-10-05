import socketio

import lcd.main

def init():
    sio = socketio.Server(lcd.main.LCD_PORT)
    app = socketio.WGSIApp(sio)

    @sio.event
    def connect(sid, environ, auth):
        print('connect', sid)

    @sio.on(lcd.main.RECEIVE_IMAGE_EVENT)
    def receive_image(sid, data):
        lcd.main.set_target_image(data["image"])

    @sio.on(lcd.main.RECEIVE_TEMPERATURE_EVENT)
    def receive_temperature(sid, data):
        lcd.main.set_temperature(data["temperature"])

    @sio.event
    def disconnect(sid):
        print('disconnect', sid)
