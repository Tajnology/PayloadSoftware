import socketio
import transmission.main

sio_send_connected = False
sio_send = None

def init():
    mgr = socketio.RedisManager('redis://localhost:' + str(transmission.main.TRANSMISSION_PORT))
    sio_recv = socketio.Server(client_manager = mgr)
    app = socketio.WSGIApp(sio_recv)

    @sio_recv.event
    def connect(sid, environ, auth):
        print('connect', sid)

    @sio_recv.on(transmission.main.RECEIVE_TD_DATA_EVENT)
    def receive_td_data(sid, data):
        ## TODO: Transmit target detection data to ground control station 
        pass

    @sio_recv.on(transmission.main.RECEIVE_AQ_DATA_EVENT)
    def receive_aq_data(sid, data):
        ## TODO: Transmit air quality data to ground control station
        pass

    @sio_recv.on(transmission.main.INIT_GCS_CLIENT_EVENT)
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

    