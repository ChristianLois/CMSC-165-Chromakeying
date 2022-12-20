import cv2 as cv
import numpy as np
 
video = cv.VideoCapture("extendedvid.mp4")
ref = cv.VideoCapture("reference.mp4")

#frame_height = int(video.get(4))
#frame_width = int(video.get(3))

out = cv.VideoWriter('output.mp4', cv.VideoWriter_fourcc(*'mp4v'), 30.0, (640,480))

print("\nProcessing video...")
while True:
 
    ret, frame = video.read()
    ret2, refFrame = ref.read()

    if not ret or not ret2:
        break
 
    frame = cv.resize(frame, (640,480))
    image = cv.resize(refFrame, (640,480))
    
    frame2 = cv.cvtColor(frame.copy(), cv.COLOR_BGR2HSV)

    # hsv bounds to detect the background
    lower = np.array([30, 142, 50])
    upper = np.array([170, 255, 255])
    
    mask = cv.inRange(frame2, lower, upper)
    mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)

    # kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,((2*21-1, 2*21-1)))
    # mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    # res = cv.bitwise_and(frame, frame, mask = mask)
    
    # f = frame - res
    f = np.where(mask == 255, image, frame)
 
    #cv.imshow("mask", f)

    # save
    out.write(f)
 
    if cv.waitKey(25) == 27:
        break

print("\nDone! Check output.mp4")

video.release()
ref.release()
out.release()
cv.destroyAllWindows()