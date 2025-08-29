# import torch
# import torchvision.models as models
# from PIL import Image
# from torchvision import transforms

# MODEL_PATH = "models/face_shape_model.pth"

# # Preprocessing transform
# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406], 
#                          [0.229, 0.224, 0.225])
# ])

# def load_model():
#     """
#     Load the entire pretrained model from the .pth file.
#     """
#     # Allow unsafe globals if using PyTorch >= 2.6
#     with torch.serialization.safe_globals([
#         torch.nn.modules.container.Sequential,
#         models.efficientnet.EfficientNet
#     ]):
#         model = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)

#     model.eval()
#     return model

# def predict_face_shape(model, pil_image):
#     """
#     Given a PIL image and a loaded model, predict face shape.
#     Returns one of: 'Oval', 'Round', 'Square', 'Heart'
#     """
#     x = transform(pil_image).unsqueeze(0)  # Add batch dimension
#     with torch.no_grad():
#         outputs = model(x)
#         _, pred = torch.max(outputs, 1)
    
#     face_shapes = ["Oval", "Round", "Square", "Heart"]
#     return face_shapes[pred.item()]

import torch
from PIL import Image
from torchvision import transforms

MODEL_PATH = "models/face_shape_model.pth"

# Preprocessing transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Lambda(lambda img: img.convert("RGB")),  # Ensure RGB
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

def load_model():
    """
    Load the entire pretrained model from the .pth file.
    This works with PyTorch 2.6+ for full model pickles.
    """
    # Use unsafe loading only if you trust the source
    model = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
    model.eval()
    return model

def predict_face_shape(model, pil_image):
    """
    Given a PIL image and a loaded model, predict face shape.
    Returns one of: 'Oval', 'Round', 'Square', 'Heart'
    """
    x = transform(pil_image).unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        outputs = model(x)
        _, pred = torch.max(outputs, 1)

    face_shapes = ["Oval", "Round", "Square", "Heart"]
    return face_shapes[pred.item()]
