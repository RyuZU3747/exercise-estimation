import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import detect
import plotting

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose    

parts = ["NOSE", "LEFT_EYE_INNER", "LEFT_EYE", "LEFT_EYE_OUTER", "RIGHT_EYE_INNER", "RIGHT_EYE", "RIGHT_EYE_OUTER",
         "LEFT_EAR", "RIGHT_EAR", "MOUTH_LEFT", "MOUTH_RIGHT", "LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_ELBOW",
         "RIGHT_ELBOW", "LEFT_WRIST", "RIGHT_WRIST", "LEFT_PINKY", "RIGHT_PINKY", "LEFT_INDEX", "RIGHT_INDEX",
         "LEFT_THUMB", "RIGHT_THUMB", "LEFT_HIP", "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE", "LEFT_ANKLE", "RIGHT_ANKLE",
         "LEFT_HEEL", "RIGHT_HEEL", "LEFT_FOOT_INDEX", "RIGHT_FOOT_INDEX"]

cap = cv2.VideoCapture(0)
fig = plt.figure(1)
fig.canvas.draw()
ax = fig.add_subplot(111, projection="3d")
current_pose = "None"


with mp_pose.Pose(
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec = mp_drawing_styles.get_default_pose_landmarks_style())
        
        
        if results.pose_landmarks:
            delta = detect.delta.get(results)
            if delta:
                current_pose = detect.detposes(results)
            
            print(detect.vector_angle(results.pose_world_landmarks.landmark[23],results.pose_world_landmarks.landmark[11]))
            plotting.plot(plt, ax, results)
           
        # image = cv2.rectangle(image, (0,0),(500,500),(0,0,0),-1)
            
        cv2.putText(image, "Current pose : "+current_pose, (10, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2, cv2.LINE_AA)    
        cv2.putText(image, "Pushup Count : "+str(detect.pushup.cnt), (10, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2, cv2.LINE_AA) 
        cv2.putText(image, "Squat Count : "+str(detect.squat.cnt), (10, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(image, "Pullup Count : "+str(detect.pullup.cnt), (10, 300),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2, cv2.LINE_AA)
        
        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break   
cap.release()