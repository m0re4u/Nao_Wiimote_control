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
            print("Turning left")
            for nao in naos:
                theta = 0.5
                nao.motion.setWalkTargetVelocity(x, y, theta, frequency)
        elif (buttons & cwiid.BTN_RIGHT):
            print("Walking right")
            for nao in naos:
                theta = -0.5
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
        elif (buttons & cwiid.BTN_A):
            print("Robot")
            for nao in naos:
                # Choregraphe bezier export in Python.
                names = list()
                times = list()
                keys = list()

                names.append("HeadPitch")
                times.append([1.26667, 3.53333, 4.33333])
                keys.append([[-0.012314, [3, -0.422222, 0], [3, 0.755556, 0]], [0.00609404, [3, -0.755556, 0], [3, 0.266667, 0]], [0.00609404, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("HeadYaw")
                times.append([1.26667, 3.53333, 4.33333])
                keys.append([[0.00762803, [3, -0.422222, 0], [3, 0.755556, 0]], [0.00762803, [3, -0.755556, 0], [3, 0.266667, 0]], [0.00762803, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("LAnklePitch")
                times.append([1.26667, 2, 3.53333, 4.33333])
                keys.append([[0.191576, [3, -0.422222, 0], [3, 0.244444, 0]], [0.205383, [3, -0.244444, 0], [3, 0.511111, 0]], [0.183907, [3, -0.511111, 0], [3, 0.266667, 0]], [0.183907, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("LAnkleRoll")
                times.append([1.26667, 2, 3.53333, 4.33333])
                keys.append([[0.0659823, [3, -0.422222, 0], [3, 0.244444, 0]], [0.0613804, [3, -0.244444, 0.00460191], [3, 0.511111, -0.00962217]], [-0.0107176, [3, -0.511111, 0], [3, 0.266667, 0]], [-0.0107176, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("LElbowRoll")
                times.append([1.26667, 2.73333, 3.53333, 4.33333])
                keys.append([[-1.4772, [3, -0.422222, 0], [3, 0.488889, 0]], [-1.55697, [3, -0.488889, 0], [3, 0.266667, 0]], [-0.010696, [3, -0.266667, 0], [3, 0.266667, 0]], [-0.010696, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("LElbowYaw")
                times.append([1.26667, 2.73333, 3.53333, 4.33333])
                keys.append([[-1.71812, [3, -0.422222, 0], [3, 0.488889, 0]], [-1.29627, [3, -0.488889, -0.323915], [3, 0.266667, 0.176681]], [-0.216335, [3, -0.266667, 0], [3, 0.266667, 0]], [-0.216335, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("LHand")
                times.append([1.26667, 3.53333, 4.33333])
                keys.append([[0.997114, [3, -0.422222, 0], [3, 0.755556, 0]], [0.995296, [3, -0.755556, 0], [3, 0.266667, 0]], [0.995296, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("LHipPitch")
                times.append([1.26667, 2, 3.53333, 4.33333])
                keys.append([[0.179256, [3, -0.422222, 0], [3, 0.244444, 0]], [0.162382, [3, -0.244444, 0.0168733], [3, 0.511111, -0.0352806]], [-0.24106, [3, -0.511111, 0], [3, 0.266667, 0]], [-0.24106, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("LHipRoll")
                times.append([1.26667, 2, 3.53333, 4.33333])
                keys.append([[0.0580999, [3, -0.422222, 0], [3, 0.244444, 0]], [0.07344, [3, -0.244444, 0], [3, 0.511111, 0]], [-0.145922, [3, -0.511111, 0], [3, 0.266667, 0]], [-0.145922, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("LHipYawPitch")
                times.append([1.26667, 2, 3.53333, 4.33333])
                keys.append([[-0.730228, [3, -0.422222, 0], [3, 0.244444, 0]], [-0.739431, [3, -0.244444, 0], [3, 0.511111, 0]], [-0.487856, [3, -0.511111, 0], [3, 0.266667, 0]], [-0.487856, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("LKneePitch")
                times.append([1.26667, 2, 3.53333, 4.33333])
                keys.append([[0.185295, [3, -0.422222, 0], [3, 0.244444, 0]], [0.169954, [3, -0.244444, 0.00146728], [3, 0.511111, -0.00306794]], [0.166886, [3, -0.511111, 0], [3, 0.266667, 0]], [0.166886, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("LShoulderPitch")
                times.append([1.26667, 2.73333, 3.53333, 4.33333])
                keys.append([[1.53089, [3, -0.422222, 0], [3, 0.488889, 0]], [0.179436, [3, -0.488889, 0], [3, 0.266667, 0]], [1.7073, [3, -0.266667, 0], [3, 0.266667, 0]], [1.7073, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("LShoulderRoll")
                times.append([1.26667, 2.73333, 3.53333, 4.33333])
                keys.append([[0.039842, [3, -0.422222, 0], [3, 0.488889, 0]], [0, [3, -0.488889, 0], [3, 0.266667, 0]], [1.35601, [3, -0.266667, 0], [3, 0.266667, 0]], [1.34374, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("LWristYaw")
                times.append([1.26667, 3.53333, 4.33333])
                keys.append([[-0.277696, [3, -0.422222, 0], [3, 0.755556, 0]], [-0.289967, [3, -0.755556, 0], [3, 0.266667, 0]], [-0.289967, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("RAnklePitch")
                times.append([1.26667, 2, 3.53333, 4.33333])
                keys.append([[-0.411138, [3, -0.422222, 0], [3, 0.244444, 0]], [-0.401935, [3, -0.244444, -0.00920312], [3, 0.511111, 0.0192429]], [0.352792, [3, -0.511111, 0], [3, 0.266667, 0]], [0.352792, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("RAnkleRoll")
                times.append([1.26667, 2, 3.53333, 4.33333])
                keys.append([[0.0322537, [3, -0.422222, 0], [3, 0.244444, 0]], [0.0337877, [3, -0.244444, -0.00153397], [3, 0.511111, 0.00320739]], [0.248547, [3, -0.511111, 0], [3, 0.266667, 0]], [0.248547, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("RElbowRoll")
                times.append([1.26667, 2.73333, 3.53333, 4.33333])
                keys.append([[1.46348, [3, -0.422222, 0], [3, 0.488889, 0]], [1.56319, [3, -0.488889, 0], [3, 0.266667, 0]], [1.54171, [3, -0.266667, 0], [3, 0.266667, 0]], [1.54171, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("RElbowYaw")
                times.append([1.26667, 2.73333, 3.53333, 4.33333])
                keys.append([[1.52015, [3, -0.422222, 0], [3, 0.488889, 0]], [1.44499, [3, -0.488889, 0], [3, 0.266667, 0]], [1.65821, [3, -0.266667, 0], [3, 0.266667, 0]], [1.65668, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("RHand")
                times.append([1.26667, 3.53333, 4.33333])
                keys.append([[1, [3, -0.422222, 0], [3, 0.755556, 0]], [1, [3, -0.755556, 0], [3, 0.266667, 0]], [1, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("RHipPitch")
                times.append([1.26667, 2, 3.53333, 4.33333])
                keys.append([[0.489289, [3, -0.422222, 0], [3, 0.244444, 0]], [0.490823, [3, -0.244444, 0], [3, 0.511111, 0]], [-0.279246, [3, -0.511111, 0], [3, 0.266667, 0]], [-0.279246, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("RHipRoll")
                times.append([1.26667, 2, 3.53333, 4.33333])
                keys.append([[-0.148778, [3, -0.422222, 0], [3, 0.244444, 0]], [-0.15338, [3, -0.244444, 0.00460191], [3, 0.511111, -0.00962217]], [-0.257691, [3, -0.511111, 0], [3, 0.266667, 0]], [-0.257691, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("RKneePitch")
                times.append([1.26667, 2, 3.53333, 4.33333])
                keys.append([[0.47666, [3, -0.422222, 0], [3, 0.244444, 0]], [0.455184, [3, -0.244444, 0.0214763], [3, 0.511111, -0.044905]], [0.0195278, [3, -0.511111, 0], [3, 0.266667, 0]], [0.0195278, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("RShoulderPitch")
                times.append([1.26667, 2.73333, 3.53333, 4.33333])
                keys.append([[0.00464395, [3, -0.422222, 0], [3, 0.488889, 0]], [2.07247, [3, -0.488889, 0], [3, 0.266667, 0]], [1.56779, [3, -0.266667, 0], [3, 0.266667, 0]], [1.56779, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("RShoulderRoll")
                times.append([1.26667, 2.73333, 3.53333, 4.33333])
                keys.append([[-0.11816, [3, -0.422222, 0], [3, 0.488889, 0]], [-0.154976, [3, -0.488889, 0.0138962], [3, 0.266667, -0.00757972]], [-0.182588, [3, -0.266667, 0], [3, 0.266667, 0]], [-0.182588, [3, -0.266667, 0], [3, 0, 0]]])

                names.append("RWristYaw")
                times.append([1.26667, 3.53333, 4.33333])
                keys.append([[0.408002, [3, -0.422222, 0], [3, 0.755556, 0]], [0.41107, [3, -0.755556, 0], [3, 0.266667, 0]], [0.41107, [3, -0.266667, 0], [3, 0, 0]]])

                try:
                  # uncomment the following line and modify the IP if you use this script outside Choregraphe.
                  # motion = ALProxy("ALMotion", IP, 9559)
                  # motion = ALProxy("ALMotion")
                  nao.motion.angleInterpolationBezier(names, times, keys)
                except BaseException, err:
                  print err
        elif (buttons & cwiid.BTN_B):
            print("Trying behavior")
            for nao in naos:
                nao.behavior.post.runBehavior('vangelis')
                print nao.behavior.post.getInstalledBehaviors()
        else:
            print("Doing nothing..")
            for nao in naos:
                x = 0
                theta = 0
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
