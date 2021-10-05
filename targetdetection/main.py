
#### EXTERNAL MODULE IMPORTS ####
import sys
from imutils.video import VideoStream

#### LOCAL IMPORTS ####
import targetdetection.ipc

#### GLOBAL CONSTANTS ####
LCD_PORT = 10000
TRANSMISSION_PORT = 10001
TRANSMIT_TD_DATA_EVENT = 'td-data'
TRANSMIT_TD_STATUS_EVENT = 'td-status'

def main(argv):
    targetdetection.ipc.init()

    vs = VideoStream(src=0).start()


if __name__ == '__main__':
    main(sys.argv[1:])