import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

def detect_face_landmarks(image):
    """Detect face landmarks and return 2D points"""
    # Convert PIL -> numpy array (RGB)
    image_np = np.array(image)
    image_rgb = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)  # Mediapipe expects RGB
    
    h, w, _ = image_rgb.shape
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True) as face_mesh:
        results = face_mesh.process(image_np)
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
            points = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks.landmark]
            return points
        else:
            return None

def classify_face_shape(points):
    """
    Simple classification of face shape using face ratios.
    Returns: 'Oval', 'Round', 'Square', 'Heart'
    """
    if points is None:
        return "No face detected"

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    face_width = max(xs) - min(xs)
    face_height = max(ys) - min(ys)
    ratio = face_height / face_width

    # Simple rule-based classification
    if ratio > 1.4:
        return "Oval"
    elif ratio > 1.2:
        return "Heart"
    elif ratio > 0.9:
        return "Square"
    else:
        return "Round"
