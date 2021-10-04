import socketio

from main import set_target_image, set_temperature, LCD_PORT, RECEIVE_IMAGE_EVENT, RECEIVE_TEMPERATURE_EVENT

def init():
    sio = socketio.Server(LCD_PORT)
    app = socketio.WGSIApp(sio)

    @sio.event
    def connect(sid, environ, auth):
        print('connect', sid)

    @sio.on(RECEIVE_IMAGE_EVENT)
    def receive_image(sid, data):
        main.set_target_image(data["image"])

    @sio.on(RECEIVE_TEMPERATURE_EVENT)
    def receive_temperature(sid, data):
        main.set_temperature(data["temperature"])

    @sio.event
    def disconnect(sid):
        print('disconnect', sid)
