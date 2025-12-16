import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def lhand(conta1, conta2, conta3, conta4, conta5, number = 0):

    if abs(conta1)>=0.15:
        number+=1
    if conta2>=0.15:
        number+=1
    if conta3>=0.20:
        number+=1
    if conta4>=0.18:
        number+=1
    if conta5>=0.09:
        number+=1

    return number

def rhand(conta1, conta2, conta3, conta4, conta5, number = 0):
    
    if abs(conta1)>=0.15:
        number+=1
    if conta2>=0.15:
        number+=1
    if conta3>=0.20:
        number+=1
    if conta4>=0.18:
        number+=1
    if conta5>=0.09:
        number+=1

    return number

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
) as hands:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for i, hand_lms in enumerate(results.multi_hand_landmarks):
                hand_label = results.multi_handedness[i].classification[0].label

                if hand_label == 'Left':
                    conta1 = hand_lms.landmark[4].x - hand_lms.landmark[9].x
                    conta2 = hand_lms.landmark[5].y - hand_lms.landmark[8].y
                    conta3 = hand_lms.landmark[9].y - hand_lms.landmark[12].y
                    conta4 = hand_lms.landmark[13].y - hand_lms.landmark[16].y
                    conta5 = hand_lms.landmark[17].y - hand_lms.landmark[20].y
                    lresult = lhand(conta1, conta2, conta3, conta4, conta5)


                if hand_label == 'Right':
                    conta1 = hand_lms.landmark[4].x - hand_lms.landmark[9].x
                    conta2 = hand_lms.landmark[5].y - hand_lms.landmark[8].y
                    conta3 = hand_lms.landmark[9].y - hand_lms.landmark[12].y
                    conta4 = hand_lms.landmark[13].y - hand_lms.landmark[16].y
                    conta5 = hand_lms.landmark[17].y - hand_lms.landmark[20].y
                    rresult = rhand(conta1, conta2, conta3, conta4, conta5)
                    print(rresult)


                cv2.putText(frame, str(lresult), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA)
                mp_draw.draw_landmarks(
                    frame, hand_lms, mp_hands.HAND_CONNECTIONS
                )

        cv2.imshow("Hands", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
