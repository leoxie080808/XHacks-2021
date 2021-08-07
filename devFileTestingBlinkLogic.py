import numpy as np
import cv2
import sys
import time
import keyboard

# define some constants for the windows part, gonna try detecting a fast blink
fastBlink = 2
doubleBlink = 0
# init the frame counters and total num of blinks
counter = 0
total = 0
totalFast = 0
lastBlinkTime = 0.0
# predictor_path = "shape_predictor_68_face_landmarks - Copy.dat"

# start the video stream thread
print("[INFO] starting video stream thread...")




# -----------------------------------------------------------------


# NEW PLAN
# 1. assume blink works, press 'q' to add a blink to the total counter
# 2. store the thread time, and the time difference to their respective list
# 3. look at the time difference between the last 3 elements in the list (or however many there are)
# 4. if each time diff is > 1.1 sec, its a single blink
#    if one time diff is < 0.7 sec, its a double blink
#    if two time diff each < 0.7 / 0.5 sec, its a triple blink
# 5. remove the elements from the list once we are done with the blink, reset the blink type

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

# ---------------------------------TESTING FOR NOW---------------------------------
while True:

    #print(time.thread_time()) #okay this works




    # so if the eyelid closes for a bit, the counter will go up
    if keyboard.is_pressed('q'):
        counter += 1

    else:  # if eyes were closed for a sufficient number of frames, then increase total
        if counter >= 1:
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
                    print("the x value is", x)
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


                elif triple > single and triple > double:
                    print("triple blink detected")
                    timeDifferenceList = timeDifferenceList[:-1]
                    print("the current list is", *timeDifferenceList)

                else:
                    print("unexpected combo")
                    print("the current list is", *timeDifferenceList)
                single = 0
                triple = 0
                double = 0


            counter = 0

            # end of blink
