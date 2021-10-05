
#### EXTERNAL MODULE IMPORTS ####
import sys

#### LOCAL IMPORTS ####
import ipc

#### GLOBAL CONSTANTS ####
LCD_PORT = 10000
TRANSMISSION_PORT = 10001
TRANSMIT_TD_DATA_EVENT = 'td-data'
TRANSMIT_TD_STATUS_EVENT = 'td-status'

def main(argv):
    ipc.init()

    pass

if __name__ == '__main__':
    main(sys.argv[1:])