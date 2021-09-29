import socketio
from main import LCD_PORT, TRANSMISSION_PORT

def init():
    lcd_sio = socketio.AsyncClient()
    transmission_sio = socketio.AsyncClient()
    
    await sio.connect('http://localhost:' + LCD_PORT)
    await sio.connect('http://localhost:' + TRANSMISSION_PORT)
