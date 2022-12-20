# Contributors: Christian Olo, Arni Mendoza, Andrea Privado, Skye Santos
# Description: Driver program for chromakeying

# Algorithm:
# 1. Divide the reference and shooted video to frames
# 2. Convert color space of each fram from shooted video to hsv from bgr
# 3. Binarize the shooted video using the lower and upper hsv (to detect green pixels)
# 4. Remove the detected green pixels and use pixels from reference video
# 5. Repeat for each frames and generate the output video

# import openCV and numpy modules
import cv2 as cv
import numpy as np
 
video = cv.VideoCapture("extendedvid.mp4")
ref = cv.VideoCapture("reference.mp4")

# size of the output video and the frames
size = (1728,810)
out = cv.VideoWriter('output.mp4', cv.VideoWriter_fourcc(*'mp4v'), 30.0, size)

print("\nProcessing video...")

# iterate through all the frames of reference and shooted video
while True:
    
    # read a frame from the shooted video and ref video
    ret, frame = video.read()
    ret2, refFrame = ref.read()

    # all frames are processes
    if not ret or not ret2:
        break
 
    frame = cv.resize(frame, size)
    image = cv.resize(refFrame, size)
    
    # covert color space from BGR to HSV to easily segment the green color
    frame2 = cv.cvtColor(frame.copy(), cv.COLOR_BGR2HSV)

    # hsv bounds to detect the background (green pixels)
    lower = np.array([30, 142, 50])
    upper = np.array([170, 255, 255])
    
    # create a mask that will binarize the green pixels (background) and non-green pixels (foreground)
    mask = cv.inRange(frame2, lower, upper)
    mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
    
    # replace backround pixels (white from mask) with pixels from the reference video
    f = np.where(mask == 255, image, frame)
 
    # cv.imshow("mask", f) # preview

    # save
    out.write(f)
 
    if cv.waitKey(25) == 27:
        break

print("\nDone! Check output.mp4")

# release the videos
video.release()
ref.release()
out.release()
cv.destroyAllWindows()