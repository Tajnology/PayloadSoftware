import socketio
import eventlet

import main

sio_send_connected = False
sio_send = None

def init():
    sio_recv = socketio.Server()
    app = socketio.WSGIApp(sio_recv)

    @sio_recv.event
    def connect(sid, environ, auth):
        print('connect', sid)

    @sio_recv.on(main.RECEIVE_TD_DATA_EVENT)
    def receive_td_data(sid, data):
        ## TODO: Transmit target detection data to ground control station 
        pass

    @sio_recv.on(main.RECEIVE_AQ_DATA_EVENT)
    def receive_aq_data(sid, data):
        print(data)
        ## TODO: Transmit air quality data to ground control station
        pass

    @sio_recv.on(main.INIT_GCS_CLIENT_EVENT)
    def init_client(sid, data):
        global sio_send
        sio_send = socketio.Client()
        sio_send.connect('http://' + data['hostname'] + ':' + data['port'])

        @sio_send.event
        def connect(sid, environ, auth):
            global sio_send_connected
            sio_send_connected = True

        @sio_send.event
        def disconnect(sid, environ, auth):
            global sio_send_connected
            sio_send_connected = False
    
    @sio_recv.event
    def disconnect(sid):
        print('disconnect', sid)

    eventlet.wsgi.server(eventlet.listen(('localhost',main.TRANSMISSION_PORT)), app)
        
    

def msg_gcs(key, value):
    if(not sio_send_connected):
        print('Transmission failed')
        return
    else:
        sio_send.emit(key,value)

    