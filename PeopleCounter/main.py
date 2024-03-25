from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to video file/stream")
ap.add_argument("-t", "--test", help="indicates running program for utility test")
#ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
#ap.add_argument("-s", "--scale", help="scale", type=float)
#ap.add_argument("-w", "--wStride", help="winStride", type=int)
#ap.add_argument("-p", "--padding", help="padding")
#ap.add_argument("-h", "--hTH", help="hitThreshold")
#ap.add_argument("-f", "finalTH", help="finalThreshold")

args = vars(ap.parse_args())

# Change these two to increase / decrease accuracy
scale = 1.05
wStride = 4


def img_detection(video, scale, wStride):

    cv2.startWindowThread()
    maxBoxes = 0

    if not args.get("test", True):
        if not args.get("video", True):
            cam = cv2.VideoCapture(0)
        else:
            cam = cv2.VideoCapture(args["video"])
        out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc('m','p','4','v'), 15., (960,540))
    else:
        cam = cv2.VideoCapture(video)

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor.getDefaultPeopleDetector())

    while True:
        ret, frame = cam.read()

        if frame is None:
            break

        #Resizes window for better detection of people
        frame = cv2.resize(frame, (960,540))
        #Sets the color of the video to grayscale for faster detection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        #Carries out the actual detection and applies bounding boxes
        boxes, weights = hog.detectMultiScale(frame, winStride=(wStride, wStride), scale=scale)
        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
        #Unifies overlapping boxes into one
        boxes = non_max_suppression(boxes, probs=None, overlapThresh=0.65)

        #Draws the bounding boxes
        for (xA, yA, xB, yB) in boxes:
            rect = cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

        #Adds text with count of people
        frame = cv2.putText(frame, "Detected: " + str(len(boxes)), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (36,255,12), 5)

        #Set maximum number of boxes
        maxBoxes = len(boxes) if len(boxes) > maxBoxes else maxBoxes

        #Shows video feed with boxes
        cv2.imshow('People Detector', frame)

        #Writes to out-file
        if not args.get("test", True):
            out.write(frame.astype('uint8'))

        #Allows us to exit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam.release()
            # out.release()
            cv2.destroyAllWindows()
            break

    #Clean up
    cam.release()
    if not args.get("test", True):
        out.release()
    cv2.destroyAllWindows()
    return maxBoxes

img_detection(args["video"], scale, wStride)