import socketio

import main

lcd_connected = False
transmission_connected = False

lcd_sio = None
transmission_sio = None

def init():
    global lcd_sio
    lcd_sio = socketio.Client()
    global transmission_sio
    transmission_sio = socketio.Client()
    
    @lcd_sio.event
    def connect():
        global lcd_connected
        lcd_connected = True

    @lcd_sio.event
    def disconnect():
        global lcd_connected
        lcd_connected = False

    @transmission_sio.event
    def connect():
        global transmission_connected
        transmission_connected = True

    @transmission_sio.event
    def disconnect():
        global transmission_connected
        transmission_connected = False

    
    lcd_sio.connect('http://localhost:'+ str(main.LCD_PORT))
    transmission_sio.connect('http://localhost:' + str(main.TRANSMISSION_PORT))


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

