import cv2
import numpy as np
import utils

curveList = []
num_items = 10 

# display = 0 : no show
# display = 1 : only show results
# display = 2 : shows entire pipeline
def getLaneCurve(img,display=2):

    imgCopy = img.copy()
    imgResult = img.copy()
    # STEP 1 : Convert the image to binary
    imgThres = utils.thresholding(img)

    # STEP 2 : Set the trackbars and warp the image to bird's eye view
    h,w,c = img.shape
    points = utils.valTrackbars() #get values of trackbars
    imgWarp = utils.warpImg(imgThres,points,w,h,inv=True)
    imgWarpPoints = utils.drawPoints(imgCopy,points)

    # STEP 3 : Pixel summation and getting the curve (direction)
    midPoint, imgHist = utils.getHistogram(imgWarp,display=True,minVal=0.5,region=4)
    basePoint, imgHist = utils.getHistogram(imgWarp,display=True,minVal=0.9,region=1)
    curveRaw = basePoint - midPoint

    # STEP 4 : Calculating the curve angle 
    curveList.append(curveRaw)
    # do not let the list exceed a certain number
    if len(curveList)>num_items:
        curveList.pop(0)

    # curve value is the average of all items in the list 
    # curve value is -ve when turn left
    curve = int(sum(curveList)/len(curveList))
    # normalization
    
    # STEP 5 : Display the results
    if display != 0:
        imgInvWarp = utils.warpImg(imgWarp, points, w, h)
        imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:h//3,0:w] = 0,0,0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
        midY = 450
        goal_reached = utils.isGoalReached(img,6000) # detect if the goal is reached
        cv2.putText(imgResult,str(curve),(w//2-80,85),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
        if goal_reached:
            cv2.putText(img,"Goal Reached",(100,85),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),3)
        cv2.line(imgResult,(w//2,midY),(w//2+(curve*3),midY),(255,0,255),5)
        cv2.line(imgResult, ((w // 2 + (curve * 3)), midY-25), (w // 2 + (curve * 3), midY+25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = w // 20
            cv2.line(imgResult, (w * x + int(curve//50 ), midY-10),
                        (w * x + int(curve//50 ), midY+10), (0, 0, 255), 2)
        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        #cv2.putText(imgResult, 'FPS '+str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230,50,50), 3);
    if display == 2:
        imgStacked = utils.stackImages(0.7,([img,imgWarpPoints,imgWarp],
                                            [imgHist,imgLaneColor,imgResult]))
        cv2.imshow('ImageStack',imgStacked)
        cv2.waitKey(1)

    elif display == 1:
        cv2.imshow('Result',imgResult)
        cv2.waitKey(1)

    curve = curve / 100
    if curve >1:
        curve = 1
    if curve<-1:
        curve = -1
 
    
    #cv2.imshow('Thres',imgCopy)
    #cv2.imshow('Warp',imgWarp)
    #cv2.resizeWindow('Warp', 500, 300)
    #cv2.imshow('WarpPoints',imgWarpPoints)
    #cv2.resizeWindow('WarpPoints', 500, 300)
    #cv2.imshow('Histogram',imgHist)
    #cv2.resizeWindow('Histogram', 500, 300)
    return curve


if __name__ == '__main__':
    cap = cv2.VideoCapture('IMG_5787.MOV')

    intialTrackbarVals = [137,0,100,240]
    utils.initializeTrackbars(intialTrackbarVals)
    frameCounter = 0
    while True:
   
        frameCounter +=1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) ==frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            frameCounter=0

        _, img = cap.read() # GET THE IMAGE
        img = cv2.resize(img,(640,480)) # RESIZE
        img = cv2.flip(img, 0)
        getLaneCurve(img)
        #cv2.imshow('Vid',img)
        #cv2.resizeWindow('Vid', 500, 300)
