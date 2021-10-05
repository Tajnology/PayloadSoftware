import socketio

import main

def init():
    mgr = socketio.RedisManager(channel='lcd')
    sio = socketio.Server(client_manager = mgr)
    app = socketio.WSGIApp(sio)

    @sio.event
    def connect(sid, environ, auth):
        print('connect', sid)

    @sio.on(main.RECEIVE_IMAGE_EVENT)
    def receive_image(sid, data):
        main.set_target_image(data["image"])

    @sio.on(main.RECEIVE_TEMPERATURE_EVENT)
    def receive_temperature(sid, data):
        main.set_temperature(data["temperature"])

    @sio.event
    def disconnect(sid):
        print('disconnect', sid)
