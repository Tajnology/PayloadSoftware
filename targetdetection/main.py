
#### EXTERNAL MODULE IMPORTS ####
import sys
from imutils.video import VideoStream, FileVideoStream
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
TRANSMIT_TD_TARGET_EVENT = 'target-detected'
ARUCO_TYPE = "DICT_5X5_100"
FRAME_WIDTH = 1000
JPEG_QUALITY = 85 # percent

ARUCO_TARGET = "aruco"
HUMAN_TARGET = "human"
BAG_TARGET = "backpack"

human_classifier = cv2.CascadeClassifier('./targetdetection/human_classifier/cascade.xml')
bag_classifier = cv2.CascadeClassifier('./targetdetection/bag_classifier/cascade.xml')

def detect_human(frame, gray, targets):
    # TODO: params to be confirmed
    human = human_classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(150,150))
    # TODO: should we change to only draw one?
    for(hx,hy,hw,hh) in human:
        cv2.rectangle(frame, (hx,hy), (hx+hw, hy+hh), (255,0,0), 2)
        cv2.putText(frame, text='HUMAN', org=(hx+hw//2-50, hy+hh+50), 
                    fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1,
                    color=(0,0,255), thickness=2)
        targets.append(HUMAN_TARGET)
    return frame

def detect_bag(frame, gray, targets):
    # TODO: params to be confirmed
    bag = bag_classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2, minSize=(75,75))
    # TODO: should we change to only draw one?
    for(bx,by,bw,bh) in bag:
        cv2.rectangle(frame, (bx,by), (bx+bw,by+bh), (0,255,0), 2)
        cv2.putText(frame, text='BAG', org=(bx+bw//2-50, by+bh+50), 
                    fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1,
                    color=(0,0,255), thickness=2)
        targets.append(BAG_TARGET)            
    return frame

def detect_aruco(frame, targets):
    markers = detect.aruco_marker(frame,ARUCO_TYPE)

    if markers != None:
        for marker in markers:
            topLeft = marker['tl']
            bottomRight = marker['br']
            # convert each of the (x, y)-coordinate pairs to integers
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            cv2.rectangle(frame, topLeft, bottomRight, (0,0,255), 2)
            # draw the ArUco marker ID on the frame
            cv2.putText(frame, str(marker['id']),
                (topLeft[0], topLeft[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0,0,255), 2)
            
            targets.append(ARUCO_TARGET + " " + str(marker['id']))
    return frame 


def main(argv):
    ipc.init()

    vs = VideoStream(src=0,resolution=(1920,1080),framerate=30).start()
    #vs = FileVideoStream(path='./test_vid_egh455.mp4', queue_size=126).start()
    #vs = cv2.VideoCapture("./test_vid_egh455.mp4")
    

    while True:
        frame = vs.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edited_frame = frame

        targets_detected = []

        #### DETECT ARUCO MARKERS
        edited_frame = detect_aruco(edited_frame, targets_detected)

        #### DETECT BODY ####
        edited_frame = detect_human(edited_frame, gray_frame, targets_detected)

        #### DETECT BACKPACK ####
        edited_frame = detect_bag(edited_frame, gray_frame, targets_detected)

        #### SEND ANNOTATED FRAME ####
        edited_frame = imutils.resize(edited_frame,width=200)

        retval, buffer = cv2.imencode('.jpg', edited_frame, [int(cv2.IMWRITE_JPEG_QUALITY),JPEG_QUALITY])
        b64img = base64.b64encode(buffer)

        for target in targets_detected:
             ipc.msg_transmission(TRANSMIT_TD_TARGET_EVENT,{'image':b64img, 'label': target })

        ipc.msg_lcd(TRANSMIT_TD_IMAGE_EVENT,{'image':b64img})
        ipc.msg_transmission(TRANSMIT_TD_IMAGE_EVENT,{'image':b64img})

        time.sleep(FRAME_INTERVAL)


if __name__ == '__main__':
    main(sys.argv[1:])
