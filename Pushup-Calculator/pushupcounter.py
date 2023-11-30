import cv2
import time
import numpy as np
import poseestimationmodule as pm

cap = cv2.VideoCapture("Videos/Myvideo.mp4")
detector = pm.poseDetector()
dir = 0
count=0
ptime = 0

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

output = cv2.VideoWriter('output1.mp4', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
while True:
    ret, frame = cap.read()
    if ret:
        frame = detector.findPose(frame)
        lmList = detector.findPosition(frame, draw=False)
        #print(lmList)
        if len(lmList)!=0:
            angle=detector.findAngle(frame, 11, 13, 15, draw=True)
            print(angle)
            # when angle is 80, % should be at 0, and when angle is 100, % should be at 100.
            # when angle is 80, bar should be at 650, and when angle is 100, bar should be at 100.
            per=np.interp(angle, (80,100), (0,100))
            color=(255, 100, 100)
            if per == 100:
                color=(100, 255, 100)
                if dir==0:
                    count+=0.5
                    dir=1
            if per == 0:
                color=(100, 100, 255)
                if dir == 1:
                    count+=0.5
                    dir=0

            # Displaying Curl Count box
            pos = [30, 450]
            ox, oy = pos[0], pos[1]
            offset = 10
            text = str(int(count))

            (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 11, 11)
            x1, y1, x2, y2 = ox - offset, oy + offset, ox + w + offset, oy - h - offset
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, text, (ox, oy), cv2.FONT_HERSHEY_PLAIN, 10, (255, 255, 255), 6)

            # Displaying the FPS
            ctime = time.time()
            fps = 1/(ctime - ptime)
            ptime = ctime
            pos = [30, 60]
            ox, oy = pos[0], pos[1]
            offset=10
            text = "FPS: " + str(int(fps))

            (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 3,3)
            x1,y1, x2, y2 = ox-offset, oy+offset, ox+w+offset, oy-h-offset
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), cv2.FILLED)
            cv2.putText(frame, text, (ox, oy), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
            frame = cv2.resize(frame, (0,0), None, fx=1.8, fy=1.0, interpolation=cv2.INTER_AREA)

            # Write the frame to the video file
            output.write(frame)

        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF==ord('1'):
            break
    else:
        break

# Release the video writer and capture objects
output.release()
cap.release()
cv2.destroyAllWindows()
