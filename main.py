import cv2
import numpy as np
import math
from pyfirmata import Arduino

#demo: https://drive.google.com/open?id=1o5wWD6clXiKC6qeON1uYP24FKBFMXq9i

class motor:
    
    def __init__(self):
        board = Arduino('COM8')
        vel   = board.get_pin('d:6:p')
        pin1  = board.get_pin('d:7:o')
        pin2  = board.get_pin('d:8:o')
    
    def sendToArduino(self, velocity):
        self.vel(velocity)
        self.pin1.write(1)
        self.pin2.write(0)
            
def processImage(camera, interval):
    
    conf, frame = camera.read()
    frameHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    qtd = 0
    
    if conf:
        
        mask   = []
        dilate = []
        c      = [[], []]
        
        for i in range(len(interval)):
            
            mask.append(cv2.inRange(frameHsv, interval[i][0], interval[i][1]))
            kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(10,5))
            dilate.append(cv2.morphologyEx(mask[i], cv2.MORPH_OPEN, kernel))
            
            cv2.imshow('dilate {}'.format(i), dilate[i])
            
            contorns, _ = cv2.findContours(dilate[i], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            if contorns is not int:
                
                bigger  = biggerCont(contorns)
                moments = cv2.moments(bigger)
                
                if moments['m00'] != 0:
                    c[i].append(int(moments['m10']/moments['m00']))
                    c[i].append(int(moments['m01']/moments['m00']))
                    qtd += 1
                    
                    if qtd == 2:  
                        cv2.line(frame, (c[0][0], c[0][1]), (c[1][0], c[1][1]), (0, 0, 255), 2)
                        cv2.imshow('frame', frame)
                        out.write(frame)
                        return c 
    
    return 0

def findAngle(h, w):
    '''
    this function calculates the tangent for 
    the values 'h' and 'w'.
    '''
    
    tan = h/(w+0.001)
    
    first = 0
    last  = 90
    
    #for i in range(8):
    #    that's necessary 'cause the binary search divides
    #    the current interval in two intervals smaller and
    #    will be necessary 7 loops for the interval to contain
    #    just two values (first and last).    
    
    for i in range(8):
        
        avg     = int((first+last)/2)
        tanReal = math.tan(math.pi/180*(avg))
        diff    = abs(tan - tanReal)
        
        if diff <= 0.01:
            return avg
        
        elif tan > tanReal:
            first = avg
        else:
            last = avg
    
    return avg

def biggerCont(contorns):
    '''
    this function receives a group of contorns and determinates
    which is bigger (area)
    '''
    
    bigger = contorn = 0
    
    for i in range(len(contorns)):
        if cv2.contourArea(contorns[i]) > bigger:
            bigger  = cv2.contourArea(contorns[i])
            contorn = contorns[i]         

    return contorn

camera = cv2.VideoCapture('output.avi')
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output2.avi',fourcc, 20.0, (640,480))

#rightMotor = motor()
#leftMotor  = motor()

while True:
    
    interval = [[np.array([135, 0, 225]), 
                 np.array([180, 41, 255])],
                [np.array([93, 54, 202]), 
                 np.array([118, 189, 255])]]
    
    points = processImage(camera, interval)
    
    if type(points) != int:
        
        height = abs(points[0][0] - points[1][0])
        width  = abs(points[0][1] - points[1][1])
        
        distance = (height**2 + width**2)**(1/2)
        
        if distance > 200:
            distance = 200
            
        angle = findAngle(height, width)
        
        velocity = (angle*0.5*int(distance/1.5))/90 + 0.5*int(distance/1.5)
        
        if points[0][0] < points[1][0]:
            #rightMotor.sendToArduino(velocity/267)
            #leftMotor.sendToArduino((distance/1.5 - velocity)/267)
            print('{:.2f} e {:.2f}'.format(2*velocity/267, 2*(distance/1.5 - velocity)/267))       
        else:
            #rightMotor.sendToArduino((distance/1.5 - velocity)/267)
            #leftMotor.sendToArduino(velocity/267)
            print('{:.2f} e {:.2f}'.format(2*(distance/1.5 - velocity)/267, 2*velocity/267))
            
    if cv2.waitKey(1) & 0xFF == 27:
        out.release()
        break
