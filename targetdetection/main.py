
#### EXTERNAL MODULE IMPORTS ####
import sys
from imutils.video import VideoStream
import imutils
import cv2
import base64
import time
import json

#### LOCAL IMPORTS ####
import ipc
import detect

#### GLOBAL CONSTANTS ####
LCD_PORT = 10000
TRANSMISSION_PORT = 10001
FRAME_INTERVAL = 0.1 # seconds
TRANSMIT_TD_IMAGE_EVENT = 'td-image'
TRANSMIT_TD_STREAMING_EVENT = 'streaming'
TRANSMIT_TD_TARGET_EVENT = 'target-detected'
ARUCO_TYPE = "DICT_5X5_100"
FRAME_WIDTH = 1000

ARUCO_TARGET = "aruco"
HUMAN_TARGET = "human"
BAG_TARGET = "backpack"

def detect_human(frame, targets):
    #TODO
    return frame

def detect_bag(frame, targets):
    #TODO
    return frame

def detect_aruco(frame, targets):
    markers = detect.aruco_marker(frame,ARUCO_TYPE)

    if markers != None:
        for marker in markers:
            topLeft = marker['tl']
            topRight = marker['tr']
            bottomLeft = marker['bl']
            bottomRight = marker['br']
            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            # draw the bounding box of the ArUCo detection
            cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
            # compute and draw the center (x, y)-coordinates of the
            # ArUco marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
            # draw the ArUco marker ID on the frame
            cv2.putText(frame, str(marker['id']),
                (topLeft[0], topLeft[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 0), 2)
            
            targets.append(ARUCO_TARGET + " " + str(marker['id']))
    return frame 


def main(argv):
    ipc.init()

    vs = VideoStream(src=0,resolution=(1920,1080),framerate=30).start()

    while True:
        frame = vs.read()
        edited_frame = frame

        targets_detected = [];

        #### DETECT ARUCO MARKERS
        edited_frame = detect_aruco(edited_frame, targets_detected)

        #### DETECT BODY ####
        edited_frame = detect_human(edited_frame, targets_detected)

        #### DETECT BACKPACK ####
        edited_frame = detect_bag(edited_frame, targets_detected)

        #### SEND ANNOTATED FRAME ####
        edited_frame = imutils.resize(edited_frame,width=200)

        retval, buffer = cv2.imencode('.jpg', edited_frame)
        b64img = base64.b64encode(buffer)

        for target in targets_detected:
             ipc.msg_transmission(TRANSMIT_TD_TARGET_EVENT,{'image':b64img, 'target': target })

        ipc.msg_lcd(TRANSMIT_TD_IMAGE_EVENT,{'image':b64img})
        ipc.msg_transmission(TRANSMIT_TD_STREAMING_EVENT,{'image':b64img})

        time.sleep(FRAME_INTERVAL)


if __name__ == '__main__':
    main(sys.argv[1:])