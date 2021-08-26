import socketio
from main import INIT_GCS_CLIENT_EVENT, TRANSMISSION_PORT, RECEIVE_TD_DATA_EVENT, RECEIVE_TD_STATUS_EVENT,  RECEIVE_AQ_DATA_EVENT, RECEIVE_AQ_STATUS_EVENT

sio_send_connected = False
sio_send = None

def init():
    sio_recv = socketio.Server()
    app = socketio.WGSIApp(sio_recv)

    @sio_recv.event
    def connect(sid, environ, auth):
        print('connect', sid)

    @sio_recv.on(RECEIVE_TD_DATA_EVENT)
    def receive_td_data(sid, data):
        ## TODO: Transmit target detection data to ground control station 
        pass

    @sio_recv.on(RECEIVE_AQ_DATA_EVENT)
    def receive_aq_data(sid, data):
        ## TODO: Transmit air quality data to ground control station
        pass

    @sio_recv.on(INIT_GCS_CLIENT_EVENT)
    def init_client(sid, data):
        sio_send = socketio.Client()
        sio_send.connect('http://' + data['hostname'] + ':' + data['port'])

        @sio_send.on('connect')
        def sio_send_connect():
            sio_send_connected = True

        @sio_send.on('disconnect')
        def sio_send_disconnect():
            sio_send_connected = False
    
    @sio_recv.event
    def disconnect(sid):
        print('disconnect', sid)
        
    

def msg_gcs(key, value):
    if(not sio_send_connected):
        print('Transmission failed')
        return
    else:
        sio_send.emit(key,value)

    