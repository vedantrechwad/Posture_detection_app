import cv2
import mediapipe as mp
import math
from playsound import playsound

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = tuple(a)
    b = tuple(b)
    c = tuple(c)
    radians = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
    angle = abs(radians*180.0/math.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize webcam
cap = cv2.VideoCapture(0)

# Function to play audio message
def play_audio():
    playsound("correct_your_posture.mp3")

# Initialize mediapipe pose instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Set flag to False initially
        left_flag = False
        right_flag = False
        
        # Detect the posture
        results = pose.process(rgb_frame)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # Get landmarks for shoulders, hips, and ankles
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            
            # Calculate angles
            angle_left = calculate_angle(left_shoulder, left_hip, left_ankle)
            angle_right = calculate_angle(right_shoulder, right_hip, right_ankle)
            
            # If angle is less than 90 degrees, set flag to True
            if angle_left < 90:
                left_flag = True
            if angle_right < 90:
                right_flag = True
                
            # Visualize the pose
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # If either flag is True, remind to correct posture and play audio message
            if left_flag or right_flag:
                cv2.putText(frame, "Correct Your Posture!", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                play_audio()
        
        # Display the frame
        cv2.imshow('Posture Detection', frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()