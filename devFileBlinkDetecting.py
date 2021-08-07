from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils

import numpy as np
import imutils
import time
import dlib
import cv2
import sys

import time


def eye_aspect_ratio(eye): 
    aPoint = dist.euclidean(eye[1], eye[5])
    bPoint = dist.euclidean(eye[2], eye[4])
    cPoint = dist.euclidean(eye[0], eye[3])

    aspectRatio = (aPoint + bPoint) / (2.0 * cPoint)
    return aspectRatio





# define two constants, one for aspect ratio to indicate blink, second for number of consecutive frames the eye must be below the threshold
eyeArThresh = 0.3 #if this is too high, might get hard to detect blinks
eyeArConsecFrames = 3

#define some constants for the windows part, gonna try detecting a fast blink
fastBlink = 2
doubleBlink = 0

# init the frame counters and total num of blinks
counter = 0
total = 0

totalFast = 0
lastBlinkTime = 0.0

predictor_path = "shape_predictor_68_face_landmarks - Copy.dat"


# initialize dlib's face detector
print("[INFO]loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

# grab the indexes of the facial landmarks for the left and right eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream thread
print("[INFO] starting video stream thread...")

vs = VideoStream(src=0).start()
fileStream = False
time.sleep(1.0)



# loop over frames from the video stream
while True: 
    if fileStream and not vs.more():
        break  # grab the frame from the threaded video file stream, resize it, and convert it to grayscale channels)
    frame = vs.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then convert the facial landmark (x, y)-coordinates to a NumPy array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        # extract the left and right eye coordinates, then use the coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        aspectRatio = (leftEAR + rightEAR) / 2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        if aspectRatio < eyeArThresh: #so if eye aspect ratio is under 0.3 for 3 frames, it registers a blink
            counter +=1


        else:
            if counter >= eyeArConsecFrames:
                blink += 1
        counter = 0

            

        cv2.putText(frame, "Blinks: {}".format(total), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "EAR: {:.2f}".format(aspectRatio), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "twoBlinks: {}".format(doubleBlink), (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)




    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()




