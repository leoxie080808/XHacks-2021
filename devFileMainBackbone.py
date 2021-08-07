import numpy as np
import cv2
import sys
import time
import keyboard
import imutils
import dlib
import sys
import ctypes # need this for the controlling windows screen

from plyer import notification
import pyautogui as gui

#imports for the blink part
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream #dont think we need this
from imutils.video import VideoStream
from imutils import face_utils


#-------------- Variables and constants

# define some constants for the windows part, gonna try detecting a fast blink
fastBlink = 2
doubleBlink = 0
# init the frame counters and total num of blinks
counter = 0
total = 0
totalFast = 0
lastBlinkTime = 0.0

# start the video stream thread
print("[INFO] starting video stream thread...")

# logic for this kinda works? except the counter will prob go up by 3 for triple, 2 for double, etc
# we can prob just divide the total counter anyways

# create ID for type of blink counter
single = 0
double = 0
triple = 0

# create list to store blink ID, and list to store time difference between blinks
blinkID = []
timeDifferenceList = []
xValueList = []

# create variable to store the thread time value
blinkThreadTime = 0.0

# create time constants for different blink, so its between multiple blinks
doubleTime = 0.5  # so if the time between 2 blinks is 0.5 sec, its a fast blink
tripleTime = 0.3  # time between 3 is 0.3 sec each, its a triple fast blink

# try this, if time after a blink is more than 0.9 sec, its the "end" of a blink sequence
endBlinkSequence = 0.99  # seconds
startBlinkSequenceFlag = False
startMomentTime = 0.0


# this stuff for the actual eye blinking part
eyeArThresh = 0.24 #if this is too high, might get hard to detect blinks       #used to be 0.3, need to change

eyeArConsecFrames = 2

#define some constants for the windows part, gonna try detecting a fast blink
fastBlink = 2
doubleBlink = 0

# init the frame counters and total num of blinks
counter = 0
total = 0

totalFast = 0
lastBlinkTime = 0.0

predictor_path = "shape_predictor_68_face_landmarks - Copy.dat"



# ---------------------Functions

# NEW PLAN
# 1. assume blink works, press 'q' to add a blink to the total counter
# 2. store the thread time, and the time difference to their respective list
# 3. look at the time difference between the last 3 elements in the list (or however many there are)
# 4. if each time diff is > 1.1 sec, its a single blink
#    if one time diff is < 0.7 sec, its a double blink
#    if two time diff each < 0.7 / 0.5 sec, its a triple blink
# 5. remove the elements from the list once we are done with the blink, reset the blink type

# some windows functions

def altTab():
    gui.keyDown('alt')
    time.sleep(.23)
    gui.press('tab')
    time.sleep(.23)
    gui.keyUp('alt')


def scrollingDown():
    print("scrolling down")
    gui.scroll(2)

def printScreen():
    gui.press("printscreen")
    notification.notify(title = "screenshot created", message = "screenshot taken!", timeout = 10)




def eye_aspect_ratio(eye):
    # compute the euclidean distances between two sets of vertical eye landmarks
    aPoint = dist.euclidean(eye[1], eye[5])
    bPoint = dist.euclidean(eye[2], eye[4])
    # compute the euclidean distance between horizontal landmarks
    cPoint = dist.euclidean(eye[0], eye[3])

    aspectRatio = (aPoint + bPoint) / (2.0 * cPoint)
    return aspectRatio

# initialize dlib's face detector
print("[INFO]loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

# grab the indexes of the facial landmarks for the left and right eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream thread
print("[INFO] starting video stream thread...")

#vs = FileVideoStream(args["video"]).start()
#fileStream = True
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
fileStream = False
time.sleep(1.0)




#here is the looping part, loop over frames from our video stream da webcam


while True:
    #if fileStream and not vs.more():
        # break

    frame = vs.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #detect faces in the grayscale frame
    rects = detector(gray, 0)

    #loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        aspectRatio = (leftEAR + rightEAR) / 2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        if aspectRatio < eyeArThresh:  # so if eye aspect ratio is under 0.3 for 3 frames, it registers a blink
            counter += 1

        else:

    # so if the eyelid closes for a bit, the counter will go up # if keyboard.is_pressed('q'): # counter += 1
    #else:  # if eyes were closed for a sufficient number of frames, then increase total
            if counter >= eyeArConsecFrames:
                startMomentTime = float(time.thread_time())
                total += 1  # a blink is detected
                blinkThreadTime = float(time.thread_time())
                # blinkTimeListThreadTime = float(time.thread_time())
                blinkID.append(blinkThreadTime)
                # blinkTimeList.append(blinkTimeListThreadTime)
                print("the", len(blinkID), "blink occurred at", blinkThreadTime)

                if len(blinkID) <= 1:
                    pass  # ensure the list doesnt pop an error out
                else:
                    # more than 1 element, calculate the time difference
                    timeDifference = (blinkID[-1] - blinkID[-2])
                    print("the time difference is", timeDifference)  # DEBUG
                    timeDifferenceList.append(timeDifference)


                    for x in timeDifferenceList[-3:]:
                        #print("the x value is", x)
                        # lets evaluate the values RIGHT NOW
                        # if x is a certain value, add one to a "single", "double", or "triple" counter
                        if x >= 1.15:
                            single += 1
                        elif x <= 0.7 and x >= 0.3:
                            double += 1
                        elif x <= 0.32 and x >= 0.1:
                            triple += 1
                        else:
                            pass #not sure if we need this end part
                    print("the current list is", *timeDifferenceList)
                    if single > double and single > triple:
                        print("single blink")
                        timeDifferenceList = timeDifferenceList[:-1]
                        print("the current list is", *timeDifferenceList)


                    elif double > single and double > triple:
                        print("double blink detected")
                        timeDifferenceList = timeDifferenceList[:-1]
                        print("the current list is", *timeDifferenceList)
                        printScreen()


                    elif triple > single and triple > double:
                        print("triple blink detected")
                        timeDifferenceList = timeDifferenceList[:-1]
                        print("the current list is", *timeDifferenceList)
                        altTab()

                    else:
                        print("unexpected combo, unsure of type")
                        print("the current list is", *timeDifferenceList)
                    single = 0
                    triple = 0
                    double = 0


                counter = 0

                # end of blink
        cv2.putText(frame, "Blinks: {}".format(total), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "EAR: {:.2f}".format(aspectRatio), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "twoBlinks: {}".format(doubleBlink), (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()






