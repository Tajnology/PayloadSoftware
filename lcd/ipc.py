import socketio

from main import set_target_image, set_temperature, LCD_PORT, RECEIVE_IMAGE_EVENT, RECEIVE_TEMPERATURE_EVENT

def init():
    sio = socketio.AsyncServer(LCD_PORT)
    app = socketio.AGSIApp(sio)

    @sio.event
    def connect(sid, environ, auth):
        print('connect', sid)

    @sio.on(RECEIVE_IMAGE_EVENT)
    def receive_image(sid, data)
        # Receive image from target detection subprogram
        pass

    @sio.on(RECEIVE_TEMPERATURE_EVENT)
        # Receive temperature data from air quality subprogram
        pass

    @sio.event
    def disconnect(sid):
        print('disconnect', sid)
