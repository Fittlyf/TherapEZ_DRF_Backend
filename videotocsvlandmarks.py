import cv2
import mediapipe as mp
import csv
import json  # Add this line to import the json module

video_path = './arthritis1.mp4'
output_csv = './output.csv'
output_json = './arthritis1.json' 

def write_landmarks_to_csv_and_json(landmarks, frame_number, csv_writer, json_data):
    frame_data = {"frame_number": frame_number, "pose_landmarks": []}

    for idx, landmark in enumerate(landmarks):
        # Write to CSV
        csv_writer.writerow([frame_number, mp_pose.PoseLandmark(idx).name, landmark.x, landmark.y, landmark.z])

        # Write to JSON
        landmark_data = {
                'x':landmark.x,
                'y':landmark.y,
                'z':landmark.z,
                'visibility':landmark.visibility
            }
        

        frame_data["pose_landmarks"].append(landmark_data)

    json_data.append(frame_data)

# Initialize MediaPipe Pose and Drawing utilities
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Open the video file
cap = cv2.VideoCapture(video_path)

frame_number = 0
csv_data = []
json_data = []  # Initialize an empty list for JSON data

# Open CSV and JSON files for writing
with open(output_csv, mode='w', newline='') as csv_file, open(output_json, mode='w') as json_file:
    csv_writer = csv.writer(csv_file)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Pose
        result = pose.process(frame_rgb)

        # Draw the pose landmarks on the frame
        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Add the landmark coordinates to the CSV and JSON files
            write_landmarks_to_csv_and_json(result.pose_landmarks.landmark, frame_number, csv_writer, json_data)

        # Display the frame
        cv2.imshow('MediaPipe Pose', frame)

        # Exit if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_number += 1

    # Write the JSON data to the JSON file
    json.dump(json_data, json_file)

# Release video capture and close CSV and JSON files
cap.release()
cv2.destroyAllWindows()
