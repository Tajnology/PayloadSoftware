import socketio
import time

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
    
    @transmission_sio.event 
    def connect():
        print('Connected to transmission')
        global transmission_connected
        transmission_connected = True

    @transmission_sio.event
    def disconnect():
        print('Disconnected from transmission')
        global transmission_connected
        transmission_connected = False

    @lcd_sio.event
    def connect():
        global lcd_connected
        lcd_connected = True

    @lcd_sio.event
    def disconnect():
        global lcd_connected
        lcd_connected = False
    
    while (not lcd_connected) or (not transmission_connected):
        try:
            lcd_sio.connect('http://127.0.0.1:' + str(main.LCD_PORT))
            transmission_sio.connect('http://127.0.0.1:' + str(main.TRANSMISSION_PORT))
        except:
            print('lcd connected ' + str(lcd_connected))
            print('transmission connected ' + str(transmission_connected))

        time.sleep(1)
    
    

    

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

