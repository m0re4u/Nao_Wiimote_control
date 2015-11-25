import argparse
import sys
import time
import math
import cwiid
from threading import Thread

from naomanager import NaoManager, DEFAULT_PORT
from naoqi import ALProxy

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

# Main program to perform the measurements
def main(args):
    # Create list of nao objects
    naos = NaoManager()
    for nao in args.nao:
        try:
            ip, port = nao.split(':')
            #naos.addnao(ip, int(port))
        except ValueError:
            ip = nao
            port = DEFAULT_PORT
            naos.addnao(ip, int(port))
    print("Connected",len(naos),"Naos")
    wm = None
    wm = connectWiimote(wm)
    x  = 0.0
    y  = 0.0
    theta  = 0.0
    frequency  = 0.3
    CommandFreq = 0.5
    print("Connected Wiimote")
    starttime = time.time()

    while True:
        buttons = wm.state['buttons']
        if (buttons & cwiid.BTN_HOME):
            print("Closing Connection")
            for nao in naos:
                print(nao.behavior.post.getInstalledBehaviors())
                wm.rumble = 1
                time.sleep(1)
                wm.rumble = 0
                nao.motion.killAll()
                nao.stop()
                wm = None
                exit()
        elif (buttons & cwiid.BTN_UP):
            print("Move forward")
            for nao in naos:
                x = 0.5
                nao.motion.setWalkTargetVelocity(x, y, theta, frequency)
        elif (buttons & cwiid.BTN_DOWN):
            print("Move backward")
            for nao in naos:
                x  = -0.5
                nao.motion.setWalkTargetVelocity(x, y, theta, frequency)
        elif (buttons & cwiid.BTN_LEFT):
            print("Walking left")
            for nao in naos:
                y = 0.5
                nao.motion.setWalkTargetVelocity(x, y, theta, frequency)
        elif (buttons & cwiid.BTN_RIGHT):
            print("Walking right")
            for nao in naos:
                y = -0.5
                nao.motion.setWalkTargetVelocity(x, y, theta, frequency)
        elif (buttons & cwiid.BTN_MINUS):
            print("Going to rest")
            for nao in naos:
                nao.motion.rest()
            print("Resting")
        elif (buttons & cwiid.BTN_PLUS):
            print("Standup")
            for nao in naos:
                nao.posture.goToPosture("StandInit", 0.5)
            print("Done standing up")
        else:
            print("Doing nothing..")
            for nao in naos:
                x = 0
                y = 0
                nao.motion.setWalkTargetVelocity(x, y, theta, frequency)
            time.sleep(CommandFreq) # sleep after every command


    # Do a simply interpolation
    #target1 = math.radians(119.5)
    #target2 = math.radians(29.5)
    #naos.motion.post.angleInterpolation(['HeadYaw', 'HeadPitch'],
    #        [[target1, -target1, 0.0], [target2, -target2, 0.0]],
    #        [[1.0, 5.0, 7.0], [1.0, 5.0, 7.0]], True)
    #naos.behavior.post.runBehavior('kecup')
    #naos.behavior.post.runBehavior('vangelis')

    # for nao in naos:
    #     nao.behavior.post.runBehavior('vangelis')


    # Wait
    #while time.time() < (starttime+10.0):
    #    time.sleep(0.1)

    # Stop logging if needed
    #naos.stop()

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--nao', action='append')
    args = parser.parse_args()

    if not args.nao:
        print('No naos to test specified!')
        sys.exit(0)

    main(args)
