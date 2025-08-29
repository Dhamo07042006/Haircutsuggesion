from PIL import Image
import os

# Map face shapes to hairstyle images
hairstyle_dict = {
    "Oval": "assets/hairstyles/oval.png",
    "Round": "assets/hairstyles/round.png",
    "Square": "assets/hairstyles/square.png",
    "Heart": "assets/hairstyles/heart.png"
}

def overlay_hairstyle(user_image, face_shape):
    """
    Overlay hairstyle PNG on top of the user's image
    """
    hairstyle_path = hairstyle_dict.get(face_shape)
    if hairstyle_path is None or not os.path.exists(hairstyle_path):
        return user_image  # fallback if no file

    # Convert to RGBA
    user_img = user_image.convert("RGBA")
    hairstyle_img = Image.open(hairstyle_path).convert("RGBA")

    # Resize hairstyle width to match user's width
    w_percent = user_img.width / hairstyle_img.width
    new_height = int(hairstyle_img.height * w_percent)
    hairstyle_img = hairstyle_img.resize((user_img.width, new_height), Image.LANCZOS)

    # Paste hairstyle at top-center
    position = (0, 0)  # top-left corner
    combined = user_img.copy()
    combined.paste(hairstyle_img, position, hairstyle_img)  # use alpha mask

    return combined
