import cv2
import mediapipe as mp
import pyautogui as pag
import time
import math
import numpy as np
frame_margin = 100 
cam_w, cam_h = 640, 480
mp_hands=mp.solutions.hands 
mp_drawing=mp.solutions.drawing_utils  #check after removing it
hands=mp_hands.Hands(max_num_hands=1,min_detection_confidence=0.7) # if flikker then increase the probability

cap=cv2.VideoCapture(0)

click_start_time=None
click_times=[]
click_cooldown=0.8
scroll_mode=False
freeze_cursor=False
screenshot_cooldown=2
last_screenshot_time=0
screen_w,screen_h=pag.size()
print("\n virtual mouse control .")
prev_screen_x,prev_screen_y=0,0

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret,frame=cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    frame=cv2.flip(frame,1)
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result=hands.process(rgb)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)
# get finger tip
            thumb_tip=hand_landmarks.landmark[4]
            index_tip=hand_landmarks.landmark[8]
            middle_tip=hand_landmarks.landmark[12]
            ring_tip=hand_landmarks.landmark[16]
            pinky_tip=hand_landmarks.landmark[20]

            fingers=[
                1 if hand_landmarks.landmark[tip].y<hand_landmarks.landmark[tip-2].y  else 0
                for tip in [8,12,16,20]
            ]
            distance=math.hypot(thumb_tip.x-index_tip.x,thumb_tip.y-index_tip.y)
            if distance<0.06:
                if not freeze_cursor:
                    freeze_cursor=True
                    click_times.append(time.time())
                    
                   # double click check
                    if len(click_times)>=2 and click_times[-1]-click_times[-2]<click_cooldown:
                        pag.doubleClick()
                        cv2.putText(frame,"Double Click",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                        click_time=[]
                    else:
                        pag.click()
                        cv2.putText(frame,"Click",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            else:
                if freeze_cursor:
                    time.sleep(0.1)
                freeze_cursor=False
            
        #move index finger tip to move cursor
            if not freeze_cursor:
                screen_x = np.interp(index_tip.x * cam_w, (frame_margin, cam_w - frame_margin), (0, screen_w))
                screen_y = np.interp(index_tip.y * cam_h, (frame_margin, cam_h - frame_margin), (0, screen_h))

                pag.moveTo(screen_x,screen_y,duration=0.02)
                prev_screen_x,prev_screen_y=screen_x,screen_y

        #scroll mode
            if sum (fingers)==4:
                scroll_mode=True
            else:
                scroll_mode=False
        #scroll action
            if scroll_mode:
                if index_tip.y<0.4:
                    pag.scroll(60)
                    cv2.putText(frame,"Scroll Up",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                elif index_tip.y>0.6:
                    pag.scroll(-60)
                    cv2.putText(frame,"Scroll Down",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        #screenshot
            if sum(fingers)==0:
                current_time=time.time()
                if current_time-last_screenshot_time>screenshot_cooldown:
                    pag.screenshot("screenshot.png")
                    last_screenshot_time=current_time
                    cv2.putText(frame,"Screenshot Taken",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.imshow("live Video",frame)
    
    if cv2.waitKey(1)==ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
