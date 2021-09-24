import getopt   # getopt.getopt()
import socket   # socket.socket(), obj.setblocking(), obj.bind(), obj.listen()
import threading
import time
import sys
from PIL import Image
import ST7735 as ST7735
from enum import Enum

# Import other files in subsystem
import ipc
import utils

# Create the display
disp = ST7735.ST7735(
    port=0,
    cs = ST7735.BG_SPI_CS_FRONT,
    dc = 9,
    backlight = 19,
    rotation = 90,
    spi_speed_hz = 4000000
)

WIDTH = disp.width
HEIGHT = disp.height

# Constants
REFRESH_INTERVAL = 0.01

TARGET_PORT = 10002
AIR_PORT = 10003

class LCDData:
    ip = utils.get_ip()
    target_image = Image.new('RGB', (WIDTH,HEIGHT), color = 'red')
    temperature = 30
    current_display = 0 # 0 = IP, 1 = Target, 2 = Air

#### MAIN ####

def main(argv):
    # Establish IPC
    target_thread = threading.Thread(target = ipc.listen_handler,args=(TARGET_PORT,ipc.handle_target_data))
    target_thread.start()

    air_thread = threading.Thread(target = ipc.listen_handler,args=(AIR_PORT,ipc.handle_air_data))
    air_thread.start()

    # Initialize the LCD.
    disp.begin()

    while(true):
        render_image = Image.new('RGB',(WIDTH,HEIGHT), color='white')

        if(current_display == 0):
            # Draw IP to display
        elif(current_display == 1):
            # Draw Target Image to display
        elif(current_display == 2):
            # Draw Temperature to display
        
        disp.display(render_image)

        LCDData.current_display = utils.get_display_mode()

        time.sleep(REFRESH_INTERVAL)

if __name__ == "__main__":
    main(sys.argv[1:])
