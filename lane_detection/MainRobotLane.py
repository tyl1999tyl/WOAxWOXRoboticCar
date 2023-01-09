from MotorModule import Motor
from LaneModule import getLaneCurve
import WebcamModule
#import cv2

##################################################
motor = Motor(2,3,4,17,22,27)
##################################################
 
def main():
 
    # get image from webcam
    img = WebcamModule.getImg()

    # get curve value of lane 
    curveVal= getLaneCurve(img,1)
 
    
    sen = 1.3  # SENSITIVITY
    maxVAl= 0.3 # MAX SPEED

    # limit the maximum speed
    if curveVal>maxVAl:curveVal = maxVAl
    if curveVal<-maxVAl: curveVal =-maxVAl
    #print(curveVal)
    # don't let the motor move if the curve value is less than a certain angle
    # so that the car won't keep moving left and right and will just move straight
    if curveVal>0:
        sen =1.7
        if curveVal<0.05: curveVal=0
    else:
        if curveVal>-0.08: curveVal=0
    motor.move(0.20,-curveVal*sen,0.05) # move the car according to the curve
    #cv2.waitKey(1)
     
 
if __name__ == '__main__':
    while True:
        main()