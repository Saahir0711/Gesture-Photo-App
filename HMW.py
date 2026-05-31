# import cv2, time, numpy as np
# import mediapipe as mp

# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
# MAIN, POP = "Gesture-Condtrolled Photo App", "Captured (ESC / Close to resume)"
# mp_draw = mp.solutions.drawing_utils

# TT = hands.landmark(mp_hands.HandLandmark.THUMB_TIP)
# TI = hands.landmark(mp_hands.HandLandmark.THUMB_IP)
# tips = [
#             hands.landmark(mp_hands.HandLandmark.INDEX_FINGER_TIP),
#             hands.landmark(mp_hands.HandLandmark.MIDDLE_FINGER_TIP),
#             hands.landmark(mp_hands.HandLandmark.RING_FINGER_TIP),
#             hands.landmark(mp_hands.HandLandmark.PINKY_TIP)]

# def detect_gesture():
    
    
#     ips = [
#             hands.landmark(mp_hands.HandLandmark.INDEX_FINGER_DIP),
#             hands.landmark(mp_hands.HandLandmark.MIDDLE_FINGER_DIP),
#             hands.landmark(mp_hands.HandLandmark.RING_FINGER_DIP),
#             hands.landmark(mp_hands.HandLandmark.PINKY_DIP)]
    
#     fingers = 0

#     for i in range(4):
#         tip_y, ip_y = (tips[i]).y, (ips[i]).y
#         if tip_y > ip_y:
#             fingers += 1
#     if TT.x < TI.x:
#         fingers += 1
    
#     return fingers

# def filter():
#     fingers = detect_gesture()
#     if not fingers:
#         fingers = 1
#     if fingers == 1:
#         return img    
#     elif fingers == 2:
#         return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     elif fingers == 3:
#         sepia_filter = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]).T

#         sepia_frame = cv2.transform(img, sepia_filter)

#         sepia_frame = np.clip(sepia_frame, 0, 255)  

#         return sepia_frame.astype(np.uint8)
#     elif fingers == 4:
#         return cv2.bitwise_not(img)
#     elif fingers == 5:
#         return cv2.GaussianBlur(img, (15, 15), 0)
    
# cap = cv2.VideoCapture(0)
# if not cap.isOpened(): print("Error: Could not access the webcam."); exit()
# paused = False ; freeze = False

# while True:
#     if paused:
#         cv2.imshow(MAIN, freeze)
#         k = cv2.waitKey(50) & 0xFF
#         if k == ord("q"): break
#         if k == 27:
#             paused = False; pinch_on = False
#             try: cv2.destroyWindow(POP)
#             except: pass
#             continue
#         try:
#             if cv2.getWindowProperty(POP, cv2.WND_PROP_VISIBLE) <= 0: paused = False; pinch_on = False
#         except cv2.error:
#             paused = False; pinch_on = False
#         continue

#     ok, img = cap.read()
#     if not ok: break
#     img = cv2.flip(img, 1); h, w = img.shape[:2]
#     res = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     now = time.time(); capture = False

#     if res.multi_hand_landmarks:
#         hand = res.multi_hand_landmarks[0]; mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNNECTIONS)
#         tx, ty = TT.x*w, TT.y*h ; ix, iy = (tips[0].x)*w, (tips[0].x)*h
#         pinch = abs(tx-ix) < 20 and abs(ty-iy) < 20
#         if pinch and not pinch_on and now-lc > 1.2: pinch_on = True; capture = True; lc = now
#         if not pinch and pinch_on: pinch_on = False
#         if not pinch:
#             filter()
    
#     out = filter()

#     if capture:
#         name = f"picture_{int(now)}.jpg"; cv2.imwrite(name, out); print("Saved:", name)
#         paused, freeze = True, out.copy(); cv2.imshow(POP, freeze)

#     cv2.imshow(MAIN, out)
#     if cv2.waitKey(1) & 0xFF == ord("q"): break

# cap.release(); cv2.destroyAllWindows(); hands.close()



import cv2, time, numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
MAIN, POP = "Gesture-Condtrolled Photo App", "Captured (ESC / Close to resume)"
mp_draw = mp.solutions.drawing_utils

# Structural constants defined globally
TT = mp_hands.HandLandmark.THUMB_TIP
TI = mp_hands.HandLandmark.THUMB_IP
tips = [
            mp_hands.HandLandmark.INDEX_FINGER_TIP,
            mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            mp_hands.HandLandmark.RING_FINGER_TIP,
            mp_hands.HandLandmark.PINKY_TIP]

ips = [
            mp_hands.HandLandmark.INDEX_FINGER_DIP,
            mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
            mp_hands.HandLandmark.RING_FINGER_DIP,
            mp_hands.HandLandmark.PINKY_DIP]

def detect_gesture(hand):
    fingers = 0

    for i in range(4):
        # Dynamically fetching live values from the active hand frame
        tip_y, ip_y = hand.landmark[tips[i]].y, hand.landmark[ips[i]].y
        if tip_y < ip_y: # Changed to '<' because Y decreases moving up the screen
            fingers += 1
            
    tt_x, ti_x = hand.landmark[TT].x, hand.landmark[TI].x
    if tt_x < ti_x:
        fingers += 1
    
    return fingers

def filter(fingers_count):
    if not fingers_count:
        fingers_count = 1
    if fingers_count == 1:
        return img    
    elif fingers_count == 2:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif fingers_count == 3:
        sepia_filter = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]).T

        sepia_frame = cv2.transform(img, sepia_filter)

        sepia_frame = np.clip(sepia_frame, 0, 255)  

        return sepia_frame.astype(np.uint8)
    elif fingers_count == 4:
        return cv2.bitwise_not(img)
    elif fingers_count == 5:
        return cv2.GaussianBlur(img, (15, 15), 0)
    return img
    
cap = cv2.VideoCapture(0)
if not cap.isOpened(): print("Error: Could not access the webcam."); exit()
paused = False ; freeze = False; pinch_on = False; lc = 0 # Pre-defined application states

while True:
    if paused:
        cv2.imshow(MAIN, freeze)
        k = cv2.waitKey(50) & 0xFF
        if k == ord("q"): break
        if k == 27:
            paused = False; pinch_on = False
            try: cv2.destroyWindow(POP)
            except: pass
            continue
        try:
            if cv2.getWindowProperty(POP, cv2.WND_PROP_VISIBLE) <= 0: paused = False; pinch_on = False
        except cv2.error:
            paused = False; pinch_on = False
        continue

    ok, img = cap.read()
    if not ok: break
    img = cv2.flip(img, 1); h, w = img.shape[:2]
    res = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    now = time.time(); capture = False; fingers_count = 1

    if res.multi_hand_landmarks:
        hand = res.multi_hand_landmarks[0]; mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)
        
        # Pull live frame positions out of the active hand container
        tx, ty = hand.landmark[TT].x*w, hand.landmark[TT].y*h 
        ix, iy = hand.landmark[tips[0]].x*w, hand.landmark[tips[0]].y*h # Fixed the duplicate .x typo here
        
        pinch = abs(tx-ix) < 20 and abs(ty-iy) < 20
        if pinch and not pinch_on and now-lc > 1.2: pinch_on = True; capture = True; lc = now
        if not pinch and pinch_on: pinch_on = False
        if not pinch:
            fingers_count = detect_gesture(hand)
    
    out = filter(fingers_count)

    if capture:
        name = f"picture_{int(now)}.jpg"; cv2.imwrite(name, out); print("Saved:", name)
        paused, freeze = True, out.copy(); cv2.imshow(POP, freeze)

    cv2.imshow(MAIN, out)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cap.release(); cv2.destroyAllWindows(); hands.close()

