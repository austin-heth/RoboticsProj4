# @ Droid Group: Lonnie Gasque, Austin Hetherington, & Ibrahim Salman

from RobotInterface import robotConnection
import serial
import time
import struct
import random
import math

random.seed(a=None)


#variables for PD controller
setPoint = 5        # Set point
prevError = 0       # Past Error
currentError = 0    # Last Error
samplingTime = .02  # Sampling Time
kp = 1.0            # Proportional Gain
kd = 0.3            # Derivative Gain


#PD controller
def pd(currentError, prevError):
    e1 =  setPoint -currentError 
    e0 =  setPoint  - prevError 
    u = (kp*e1) + (kd*(e1 - e0)/samplingTime)
    return int(u)

#rotate function to be used in Task2
def rotate(right, left):
        #generate a random integer between -30 and 30
        randAngle = random.randrange(-30, 30, 1)
        #add randAngle to 180 for the total angle needing to be rotated
        angleRotate = randAngle + 180
        #checks if both right and left side sensors were activated
        if right and left:
                #chooses a random rotation direction
                if randAngle % 2 == 0:
                        #execute a clockwise rotation
                        r.driveDirect(slowSpeed, -slowSpeed)
                        #keep rotating until angleRotate is achieved
                        while angleRotate > 0:
                                time.sleep(0.0125)
                                angleRotate = angleRotate + r.angle()
                        #execute a stop drive command
                        r.driveDirect(0, 0)
                else:#will execute a counterclockwise rotation
                        r.driveDirect(-slowSpeed, slowSpeed)
                        #keep rotating until angleRotate is achieved
                        while angleRotate > 0:
                                time.sleep(0.0125)
                                angleRotate = angleRotate - r.angle()
                        #execute a stop drive command
                        r.driveDirect(0, 0)
        #case for the left sensor being activated, hence clockwise rotation
        elif left:
                #execute a clockwise rotation
                r.driveDirect(slowSpeed, -slowSpeed)
                #keep rotating until angleRotate is achieved
                while angleRotate > 0:
                        time.sleep(0.0125)
                        angleRotate = angleRotate + r.angle()
                #execute a stop drive command
                r.driveDirect(0, 0)
        #else right sensor active, hence counterclockwise rotation
        else:
                #executes a counterclockwise rotation
                r.driveDirect(-slowSpeed, slowSpeed)
                #keep rotating until angleRotate is achieved
                while angleRotate > 0:
                        time.sleep(0.0125)
                        angleRotate = angleRotate - r.angle()
                #execute a stop drive command
                r.driveDirect(0, 0)


#main
r = robotConnection()
r.start()
r.passive()
r.safe()
r.angle()
r.distance()
time.sleep(0.0125)
r.warningSong()
r.successSong1()
r.successSong2()

#Robot state
robotState = 0

# booleans for the while loop.
# True; if robot not charging on dock
run = True
# True; if Dock sensored 
Dock = False

#if robot is already charging; play song and quit.
if (r.readDock() != 0):
    print str("Robot already Charging!");
    time.sleep(0.0125)
    r.song3()
    r.stop()
    run = False
    print str("");
    print str("See you later!");
    exit()
r.song1()

#set slow speed at 50 mm/s
slowSpeed = 50

#angle rotated variable
angle = 0

#infinite loop that contains Task 2 requirements

while run:
        #boolean variables used for storing sensor data
        r_Bump = False
        l_Bump = False
        r_WheelDrop = False
        l_WheelDrop = False
        r_Cliff = False
        r_FrontCliff = False
        l_Cliff = False
        l_FrontCliff = False
        cleanPress = False
        stateChanged = False

        #checks all sensors
        cleanPress = r.readButton()
        r_Bump = r.readBumpRight()
        l_Bump = r.readBumpLeft()
        r_WheelDrop = r.readWheelDropRight()
        l_WheelDrop = r.readWheelDropLeft()
        r_Cliff = r.readCliffRight()
        r_FrontCliff = r.readCliffFrontRight()
        l_Cliff = r.readCliffLeft()
        l_FrontCliff = r.readCliffFrontLeft()
        lt_Right = r. readLightRight ()
        lt_FrontRight = r.readLightFrontRight()
        lt_CenterRight = r.readLightCenterRight()
        omni_IR=r.readIrOmni()
        r_IR=r.readRightIR()
        l_IR=r.readLeftIR()
        dock = r.readDock()
        angle = angle + r.angle()
        
        # Error calculation for PD 
        prevError=currentError
        currentError=(lt_Right+lt_CenterRight+lt_FrontRight)/3
       
        #check if dock is sensed 
        if omni_IR != 0 or r_IR != 0 or l_IR != 0:
            Dock = True
            angle = 0

        #checks if robot is within force field, and if so, changes to slowSpeed
        if (omni_IR==161 or r_IR == 161 or l_IR == 161):
            slowSpeed = 25

        #check if robot is charging on the dock
        if (dock != 0):
            print str("Robot Charging!");
            r.driveDirect(0,0)
            r.song2()
            print str("")
            print str("See you later!")
            exit()
    
        #robot is stopped
        if robotState == 0:
                #check for whether the clean button has been pressed
                if cleanPress == True:# mabye add (and Dock == False)
                        #roomba starts driving forward if clean button is pressed
                        r.driveDirect(slowSpeed, slowSpeed)
                        robotState = 1
                        stateChanged = True

        #robot has been moving
        if robotState == 1 and not stateChanged:
                #check for whether the clean button has been pressed
                if cleanPress == True:
                        #roomba must stop
                        r.driveDirect(0, 0)
                        robotState = 0
                        stateChanged = True
                #else checks for wheel drops
                elif r_WheelDrop or l_WheelDrop:
                        #roomba stops and plays warning song
                        r.driveDirect(0, 0)
                        robotState = 0
                        time.sleep(0.0125)
                        r.song4()
                        stateChanged = True
                #else checks for cliff sensors while not on dock
                elif (r_Cliff or r_FrontCliff or l_Cliff or l_FrontCliff) and dock != 2:
                        #roomba stops, backs up quickly, and rotates accordingly
                        r.driveDirect(0, 0)
                        robotState = 0
                        stateChanged = True
                        #executes a quick backwards movement
                        r.driveDirect(-slowSpeed, -slowSpeed)
                        time.sleep(0.5)
                        r.driveDirect(0, 0)
                        #creates right and left Cliff side booleans
                        rightCliffSide = False
                        leftCliffSide = False
                        #condenses right and right front cliff sensor booleans
                        if r_Cliff or r_FrontCliff:
                                rightCliffSide = True
                        if l_Cliff or l_FrontCliff:
                                leftCliffSide = True
                        rotate(rightCliffSide, leftCliffSide)
                        #after rotate is completed, begin moving forward again
                        r.driveDirect(slowSpeed, slowSpeed)
                        robotState = 1        
                #else check for bumper sensors
                elif (r_Bump or l_Bump) and Dock == False :
                        #roomba stops and rotates accordingly
                        r.driveDirect(0, 0)
                        robotState = 0
                        stateChanged = True
                        rotate(r_Bump, l_Bump)
                        #after rotate is completed, begin moving forward again
                        r.driveDirect(slowSpeed, slowSpeed)
                        robotState = 1
                
                #Wall Following 
                elif lt_Right==0 and Dock == False:
                    r.driveDirect(100,10)
                    time.sleep(samplingTime)           
                elif pd(currentError,prevError)<20 and robotState==1 and Dock == False:
                    r.driveDirect(slowSpeed+pd(currentError,prevError),slowSpeed-pd(currentError,prevError))
                    time.sleep(samplingTime)
                elif (pd(currentError,prevError) >= 8 and pd(currentError,prevError) <= 9) and robotState==1 and Dock == False:
                    r.driveDirect(slowSpeed,slowSpeed)
                    time.sleep(samplingTime)  
                elif Dock == False:
                        r.driveDirect(slowSpeed-pd(currentError,prevError),slowSpeed+pd(currentError,prevError))
                        time.sleep(samplingTime)
                
                #Dock Finding 
                # Alteranate Bumping DEF
                elif(r_Bump == True or l_Bump == True) and dock == 0:
                    r.driveDirect(-slowSpeed,-slowSpeed)
                    time.sleep(0.0125)
                #IR sensors conditions    
                elif (omni_IR==164 or r_IR == 164 or l_IR == 164) and Dock==True and dock == 0:
                    r.driveDirect(slowSpeed,0)
                    time.sleep(0.0125)
                elif (omni_IR==168 or r_IR == 168 or l_IR == 168)and Dock==True and dock == 0:
                    r.driveDirect(0,slowSpeed)
                    time.sleep(0.0125)
                elif (omni_IR==172 or r_IR == 172 or l_IR == 172)and Dock==True and dock == 0:
                    r.driveDirect(slowSpeed,slowSpeed)
                    time.sleep(0.0125)
                #case where robot has gone in a circle and not picked up a new infrared sensor reading
                elif angle >= 360 and Dock==True:
                    r.driveDirect(slowSpeed,slowSpeed)
                    time.sleep(0.0125)
                    angle = 0

                
                       

                        
