
import streamlit as st
from PIL import Image
import cv2
import os
import time
from utils.predict_face_shape import load_model, predict_face_shape
import requests
from io import BytesIO

st.title("💇‍♂️ Face Shape & Hairstyle Demo (Webcam or Upload)")

# Load pretrained model once
model = load_model()

# Local hairstyle mappings
hairstyle_options = {
    "Oval": ["oval1.png", "oval2.png", "oval3.png"],
    "Round": ["round1.png", "round2.png", "round3.png"],
    "Square": ["square1.png", "square2.png", "square3.png"],
    "Heart": ["heart1.png", "heart2.png", "heart3.png"]
}

hairstyle_names = {
    "Oval": ["High Fade", "Slicked Back", "Quiff"],
    "Round": ["Taper Fade", "Side Swept Quiff", "Textured Quiff with Mid-to-High Fade"],
    "Square": ["Curly Taper Fade", "Medium Side Part", "Undercut Quiff"],
    "Heart": ["Low Fade Pompadour", "French Crop Fade", "Short Straight Mocha"]
}

# Online hairstyle suggestions (example URLs)
online_hairstyles = {
    "Oval": [
        "https://www.viningsbarber.com/blog/haircuts-for-men-with-oval-faces",
        "http://mendeserve.com/blogs/hair/best-trending-oval-face-hairstyles-for-men",
        "https://www.mensxp.com/grooming/hairstyle/144579-hairstyles-for-oval-faces-for-men.html"
    ],
    "Round": [
        "https://menshaircuts.com/round-face-haircuts-men/",
        "http://mendeserve.com/blogs/hair/top-trending-round-face-hairstyles-for-men-in-2024",
        "https://haircutinspiration.com/best-haircuts-for-round-faces-men/"
    ],
    "Square": [
        "http://mendeserve.com/blogs/hair/top-hairstyles-for-men-with-square-shape-face",
        "https://thevou.com/blog/hairstyle-for-square-face-male/",
        "https://gatsby.sg/mens-lifestyle/10-hairstyles-for-men-with-square-face-shapes-in-2025/"
    ],
    "Heart": [
        "https://www.bosshunting.com.au/style/grooming/heart-shaped-face-hairstyles/",
        "https://thevou.com/blog/haircuts-for-heart-shaped-faces/",
        "http://mendeserve.com/blogs/hair/haircuts-for-heart-shaped-faces-for-men"
    ]
}

# Choice: Webcam or Upload
option = st.radio("Choose input method:", ["Webcam", "Upload Image"])
FRAME_WINDOW = st.image([])

face_shape = None
detected_frame = None

if option == "Webcam":
    st.info("Position your face in front of the camera. The model will detect your face shape in 5 seconds.")
    cap = cv2.VideoCapture(0)
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Camera not available")
            break

        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(frame_rgb)

        # Predict face shape
        temp_shape = predict_face_shape(model, img_pil)
        if temp_shape is not None:
            face_shape = temp_shape
            detected_frame = img_pil

        # Show live webcam feed
        FRAME_WINDOW.image(frame_rgb, use_container_width=True)

        # Stop after 5 seconds
        if time.time() - start_time > 5:
            break

    cap.release()

elif option == "Upload Image":
    uploaded_file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img_pil = Image.open(uploaded_file)
        detected_frame = img_pil

        # Predict face shape
        face_shape = predict_face_shape(model, img_pil)
        st.image(img_pil, caption="Uploaded Image", use_container_width=True)

# Show results and hairstyles
if face_shape is None:
    st.warning("No face detected. Please try again.")
elif detected_frame is not None:
    st.success(f"Detected Face Shape: **{face_shape}**")

    st.markdown("### 🎨 Local Hairstyle Suggestions")
    suggestions = hairstyle_options.get(face_shape, [])
    names = hairstyle_names.get(face_shape, [])

    cols = st.columns(3)
    for i, col in enumerate(cols):
        if i < len(suggestions):
            hairstyle_path = os.path.join("assets/hairstyles", suggestions[i])
            if os.path.exists(hairstyle_path):
                img = Image.open(hairstyle_path)
                col.image(img, use_container_width=True)
                col.caption(names[i])
            else:
                col.write("Image not found")

    st.markdown("### 🌐 Online Hairstyle References")
    online_urls = online_hairstyles.get(face_shape, [])
    for url in online_urls:
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            st.image(img, use_column_width=True)
        except:
            st.write(f"Online Reference: {url}")

# import streamlit as st
# from PIL import Image
# import cv2
# import os
# import time
# import platform
# from utils.predict_face_shape import load_model, predict_face_shape

# st.title("💇‍♂️ Face Shape & Hairstyle Demo")

# # Load pretrained model once
# model = load_model()

# # Local hairstyle mappings
# hairstyle_options = {
#     "Oval": ["oval1.png", "oval2.png", "oval3.png"],
#     "Round": ["round1.png", "round2.png", "round3.png"],
#     "Square": ["square1.png", "square2.png", "square3.png"],
#     "Heart": ["heart1.png", "heart2.png", "heart3.png"]
# }

# hairstyle_names = {
#     "Oval": ["High Fade", "Slicked Back", "Quiff"],
#     "Round": ["Taper Fade", "Side Swept Quiff", "Textured Quiff with Mid-to-High Fade"],
#     "Square": ["Curly Taper Fade", "Medium Side Part", "Undercut Quiff"],
#     "Heart": ["Low Fade Pompadour", "French Crop Fade", "Short Straight Mocha"]
# }

# # Online hairstyle references (articles or galleries)
# online_hairstyles = {
#     "Oval": [
#         "https://www.viningsbarber.com/blog/haircuts-for-men-with-oval-faces",
#         "http://mendeserve.com/blogs/hair/best-trending-oval-face-hairstyles-for-men",
#         "https://www.mensxp.com/grooming/hairstyle/144579-hairstyles-for-oval-faces-for-men.html"
#     ],
#     "Round": [
#         "https://menshaircuts.com/round-face-haircuts-men/",
#         "http://mendeserve.com/blogs/hair/top-trending-round-face-hairstyles-for-men-in-2024",
#         "https://haircutinspiration.com/best-haircuts-for-round-faces-men/"
#     ],
#     "Square": [
#         "http://mendeserve.com/blogs/hair/top-hairstyles-for-men-with-square-shape-face",
#         "https://thevou.com/blog/hairstyle-for-square-face-male/",
#         "https://gatsby.sg/mens-lifestyle/10-hairstyles-for-men-with-square-face-shapes-in-2025/"
#     ],
#     "Heart": [
#         "https://www.bosshunting.com.au/style/grooming/heart-shaped-face-hairstyles/",
#         "https://thevou.com/blog/haircuts-for-heart-shaped-faces/",
#         "http://mendeserve.com/blogs/hair/haircuts-for-heart-shaped-faces-for-men"
#     ]
# }

# # Detect if running locally
# def running_locally():
#     return "Windows" in platform.platform() or "Darwin" in platform.platform()

# # Choice: Webcam or Upload
# if running_locally():
#     option = st.radio("Choose input method:", ["Webcam", "Upload Image"])
# else:
#     st.info("⚠️ Webcam not supported in deployed/mobile version. Please upload an image instead.")
#     option = "Upload Image"

# FRAME_WINDOW = st.image([])
# face_shape = None
# detected_frame = None

# if option == "Webcam":
#     st.info("📸 Position your face in front of the camera. The model will auto-detect in 5 seconds.")
#     cap = cv2.VideoCapture(0)
#     start_time = time.time()

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             st.warning("⚠️ Camera not available")
#             break

#         # Convert BGR to RGB
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         img_pil = Image.fromarray(frame_rgb)

#         # Predict face shape
#         temp_shape = predict_face_shape(model, img_pil)
#         if temp_shape is not None:
#             face_shape = temp_shape
#             detected_frame = img_pil

#         # Show live webcam feed
#         FRAME_WINDOW.image(frame_rgb, use_container_width=True)

#         # Stop after 5 seconds
#         if time.time() - start_time > 5:
#             break

#     cap.release()

# elif option == "Upload Image":
#     uploaded_file = st.file_uploader("📂 Upload your image", type=["jpg", "jpeg", "png"])
#     if uploaded_file is not None:
#         img_pil = Image.open(uploaded_file)
#         detected_frame = img_pil

#         # Predict face shape
#         face_shape = predict_face_shape(model, img_pil)
#         st.image(img_pil, caption="Uploaded Image", use_container_width=True)

# # Show results and hairstyles
# if face_shape is None:
#     st.warning("🙁 No face detected. Please try again.")
# elif detected_frame is not None:
#     st.success(f"✅ Detected Face Shape: **{face_shape}**")

#     st.markdown("### 🎨 Local Hairstyle Suggestions")
#     suggestions = hairstyle_options.get(face_shape, [])
#     names = hairstyle_names.get(face_shape, [])

#     cols = st.columns(3)
#     for i, col in enumerate(cols):
#         if i < len(suggestions):
#             hairstyle_path = os.path.join("assets/hairstyles", suggestions[i])
#             if os.path.exists(hairstyle_path):
#                 img = Image.open(hairstyle_path)
#                 col.image(img, use_container_width=True)
#                 col.caption(names[i])
#             else:
#                 col.write("Image not found")

#     st.markdown("### 🌐 Online Hairstyle References")
#     online_urls = online_hairstyles.get(face_shape, [])
#     for i, url in enumerate(online_urls, start=1):
#         st.markdown(f"[🔗 Hairstyle Reference {i}]({url})")
