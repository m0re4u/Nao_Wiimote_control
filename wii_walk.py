# -*- encoding: UTF-8 -*-

'''Walk: Small example to make Nao walk'''
import sys
import motion
import time
from naoqi import ALProxy
import cwiid

class wiiController(self):
    def StiffnessOn(proxy):
        # We use the "Body" name to signify the collection of all joints
        pNames = "Body"
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

    def StiffnessOff(proxy):
        pNames = "Body"
        pStiffnessLists = 0.0
        pTimeLists = 1.0
        proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

    def connectWiimote(wm):
        i = 0
        print 'Press 1+2 on your Wiimote now...'
        while not wm:
            try:
                wm = cwiid.Wiimote()
                print("Connected")
            except RuntimeError:
                if(i>5):
                    print("Cannot connect to Wiimote")
                    quit()
                print("Failed attempt",i)
                i += 1

        wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
        wm.led = 1
        return wm


    def main(robotIP):
        # Init proxies.
        try:
            motionProxy = ALProxy("ALMotion", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e

        try:
            postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e

        # Set NAO in Stiffness On
        StiffnessOn(motionProxy)

        # Send NAO to Pose Init
        postureProxy.goToPosture("StandInit", 0.5)

        #####################
        ## Enable arms control by Walk algorithm
        #####################
        motionProxy.setWalkArmsEnabled(True, True)
        #~ motionProxy.setWalkArmsEnabled(False, False)

        #####################
        ## FOOT CONTACT PROTECTION
        #####################
        #~ motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", False]])
        motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

        # Movement! ------
        x  = 0.0
        y  = 0.0
        theta  = 0.0
        frequency  = 0.3
        CommandFreq = 0.5
        print("Ready for moving")
        while True:
            buttons = wm.state['buttons']

            if (buttons & cwiid.BTN_HOME):
                print("Closing Connection")
                wm.rumble = 1
                time.sleep(1)
                wm.rumble = 0
                motionProxy.killAll()
                motionProxy.rest()
                exit()
            elif (buttons & cwiid.BTN_UP):
                print("Move forward")
                x = 0.5
                motionProxy.setWalkTargetVelocity(x, y, theta, frequency)
            elif (buttons & cwiid.BTN_DOWN):
                print("Move backward")
                x  = -0.5
                motionProxy.setWalkTargetVelocity(x, y, theta, frequency)
            elif (buttons & cwiid.BTN_LEFT):
                print("Walking left")
                y = 0.5
                motionProxy.setWalkTargetVelocity(x, y, theta, frequency)
            elif (buttons & cwiid.BTN_RIGHT):
                print("Walking right")
                y = -0.5
                motionProxy.setWalkTargetVelocity(x, y, theta, frequency)
            elif (buttons & cwiid.BTN_MINUS):
                print("Going to rest")
                motionProxy.rest()
            elif (buttons & cwiid.BTN_PLUS):
                print("Standup")
                postureProxy.goToPosture("StandInit", 0.5)
            else:
                print("Doing nothing..")
                x = 0
                y = 0
                motionProxy.setWalkTargetVelocity(x, y, theta, frequency)
            time.sleep(CommandFreq) # sleep after every command

if __name__ == "__main__":
    robotIp = "192.168.1.49"

    if len(sys.argv) <= 1:
        print "Usage: python wii_walk.py robotIP (optional default: 192.168.1.49)"
    else:
        robotIp = sys.argv[1]
    wm = None
    wm = connectWiimote(wm)
    main(robotIp)
