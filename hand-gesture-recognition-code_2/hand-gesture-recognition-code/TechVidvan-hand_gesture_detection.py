# TechVidvan hand Gesture Recognizer
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model



class handGesture:


    def __init__(self):

# initialize mediapipe
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mpDraw = mp.solutions.drawing_utils

        # Load the gesture recognizer model
        self.model = load_model('mp_hand_gesture')

# Load class names
        self.f = open('gesture.names', 'r')
        self.classNames = self.f.read().split('\n')
        self.f.close()
        print(self.classNames)


# Initialize the webcam
        self.cap = cv2.VideoCapture(0)
    def run(self):

        while True:
            # Read each frame from the webcam
            _, frame = self.cap.read()
        
            x, y, c = frame.shape
        
            # Flip the frame vertically
            frame = cv2.flip(frame, 1)
            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
            # Get hand landmark prediction
            result = self.hands.process(framergb)
            #print(result)
            
            className = ''
        
            # post process the result
            if result.multi_hand_landmarks:
                landmarks = []
                for handslms in result.multi_hand_landmarks:
                    for lm in handslms.landmark:
                        # print(id, lm)
                        lmx = int(lm.x * x)
                        lmy = int(lm.y * y)
                        landmarks.append([lmx, lmy])
        
                    # Drawing landmarks on frames
                    self.mpDraw.draw_landmarks(frame, handslms, self.mpHands.HAND_CONNECTIONS)
        
                    # Predict gesture
                    prediction = self.model.predict([landmarks])
                    # print(prediction)
                    classID = np.argmax(prediction)
                    className = self.classNames[classID]
        
            # show the prediction on the frame
            cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                           1, (0,0,255), 2, cv2.LINE_AA)
        
            if className == "thumbs up":
                print("it is okay")
        
            # Show the final output
            cv2.imshow("Output", frame) 
        
            if cv2.waitKey(1) == ord('q'):
                break
    
        

