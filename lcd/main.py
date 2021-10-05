#### EXTERNAL MODULE IMPORTS ####
import getopt   # getopt.getopt()
import time
import sys
import os
from threading import Lock
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from enum import Enum
import ST7735 as ST7735

#### LOCAL IMPORTS ####
import ipc
import utils

#### LCD HARDWARE DECLARATION ####
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


#### GLOBAL CONSTANTS ####
LCD_PORT = 10000
REFRESH_INTERVAL = 0.01 # seconds
RECEIVE_IMAGE_EVENT = 'td-image'
RECEIVE_TEMPERATURE_EVENT = 'air-data'
DISPLAY_MODE_FILE = '/home/payload/Code/PayloadSoftware/displaymode/display_mode.txt'
FONT_SIZE = 20


#### LOAD FONT ####
font = ImageFont.truetype("Roboto-Medium.ttf",size=15)


#### GLOBAL VARIABLES ####
ip = utils.get_ip()
target_image = None
target_image_mutex = Lock()
temperature = None
temperature_mutex = Lock()
current_display = 0 # 0 = IP, 1 = Target, 2 = Air

render_image = Image.new('RGB',(WIDTH,HEIGHT), color='white') # Create blank image
draw = ImageDraw.Draw(render_image)

#### MAIN PROCEDURE ####
def main(argv):
    # Establish Inter-Process Communication
    ipc.init()

    disp.begin() # Initialize the LCD.

    while(True):
        current_display = utils.get_display_mode(DISPLAY_MODE_FILE)

        # Render and display image on LCD
        if(current_display == 0):
            pass
            # Draw IP to display
        elif(current_display == 1):
            if(target_image != None):
                target_image_mutex.acquire()

                try:
                    pass
                    # Draw Target Image to display
                finally:
                    target_image_mutex.release()
            else:
                pass
                # Draw a 'no image found icon'
        elif(current_display == 2):
            if(temperature != None):
                temperature_mutex.acquire()

                try:
                    pass
                    # Draw Temperature to display
                finally:
                    temperature_mutex.release()
        disp.display(render_image)

        time.sleep(REFRESH_INTERVAL)


#### SYNCHRONISED ACCESSORS ####
def set_target_image(image):
    target_image_mutex.acquire()
    try:
        target_image = image
    finally:
        target_image_mutex.release()

def set_temperature(temp):
    temperature_mutex.acquire()

    try:
        temperature = temp
    finally:
        temperature_mutex.release()


#### ENTRY POINT ####
if __name__ == "__main__":
    main(sys.argv[1:])
