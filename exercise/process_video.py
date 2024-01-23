import cv2
import mediapipe as mp
import json 
import os

def process_video_and_write_to_json(video_path, output_json):
    # Initialize MediaPipe Pose and Drawing utilities
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose()

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    frame_number = 0
    json_data = []  # Initialize an empty list for JSON data

    # Create the directory for the output JSON file if it doesn't exist
    output_dir = os.path.dirname(output_json)
    os.makedirs(output_dir, exist_ok=True)

    # Open JSON file for writing
    with open(output_json, mode='w') as json_file:
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

                # Add the landmark coordinates to the JSON file
                write_landmarks_to_json(result.pose_landmarks.landmark, frame_number, json_data)

            # Display the frame
            cv2.imshow('MediaPipe Pose', frame)

            # Exit if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            frame_number += 1

        # Write the JSON data to the JSON file
        json.dump(json_data, json_file)

    # Release video capture and close JSON file
    cap.release()
    cv2.destroyAllWindows()

def write_landmarks_to_json(landmarks, frame_number, json_data):
    frame_data = {"frame_number": frame_number, "pose_landmarks": []}

    for idx, landmark in enumerate(landmarks):
        # Write to JSON
        landmark_data = {
                'x': landmark.x,
                'y': landmark.y,
                'z': landmark.z,
                'visibility': landmark.visibility
            }

        frame_data["pose_landmarks"].append(landmark_data)

    json_data.append(frame_data)

# Example usage
# video_path = './arthritis9.mp4'
# output_json = './arthritis9.json' 
# process_video_and_write_to_json(video_path, output_json)
