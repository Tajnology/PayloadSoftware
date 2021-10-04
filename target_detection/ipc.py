import socketio
from main import LCD_PORT, TRANSMISSION_PORT

lcd_connected = False
transmission_connected = False

lcd_sio = None
transmission_sio = None

def init():
    lcd_sio = socketio.Client()
    transmission_sio = socketio.Client()
    
    sio.connect('http://localhost:' + LCD_PORT)
    sio.connect('http://localhost:' + TRANSMISSION_PORT)

    @lcd_sio.on('connect')
    def lcd_connect():
        lcd_connected = True

    @lcd_sio.on('disconnect')
    def lcd_disconnect():
        lcd_connected = False

    @transmission_sio.on('connect')
    def transmission_connect():
        transmission_connected = True

    @transmission_sio.on('disconnect')
    def transmission_disconnect():
        transmission_connected = False

def msg_transmission(key,value):
    if(not transmission_connected):
        print('Connection failed')
        return
    else:
        transmission_sio.emit(key,value)

def msg_lcd(key,value):
    if(not lcd_connected):
        print('Connection failed')
        return
    else:
        lcd_sio.emit(key,value)
