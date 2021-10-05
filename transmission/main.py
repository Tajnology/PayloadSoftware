import sys

#### LOCAL IMPORTS ####

import transmission.ipc

#### GLOBAL CONSTANTS ####
TRANSMISSION_PORT = 10001
INIT_GCS_CLIENT_EVENT = 'gcs-init'
RECEIVE_TD_DATA_EVENT = 'td-data'
RECEIVE_TD_STATUS_EVENT = 'td-status'
RECEIVE_AQ_DATA_EVENT = 'air-data'
RECEIVE_AQ_STATUS_EVENT = 'air-data'


def main(argv):
    transmission.ipc.init()

if __name__ == "__main__":
    main(sys.argv[1:])
