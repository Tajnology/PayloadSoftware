import sys
import time

#### LOCAL IMPORTS ####


import ipc

#### GLOBAL CONSTANTS ####
TRANSMISSION_PORT = 10001
INIT_GCS_CLIENT_EVENT = 'gcs-init'
TD_DATA_EVENT = 'td-data'
TD_IMAGE_EVENT = 'td-image'
TD_LOG_EVENT = 'td-logtarget'
AQ_DATA_EVENT = 'air-data'
AQ_STATUS_EVENT = 'air-status'


def main(argv):
    ipc.init()

    while(True):
        time.sleep(0.1)

if __name__ == "__main__":
    main(sys.argv[1:])
