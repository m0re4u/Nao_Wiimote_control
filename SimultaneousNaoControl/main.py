import argparse
import sys
import time
import math
from threading import Thread

from naomanager import NaoManager, DEFAULT_PORT
from naoqi import ALProxy

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
            

    starttime = time.time()

    for nao in naos:
       nao.behavior.post.runBehavior('standup')
   
    time.sleep(15.0)

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
    
    
