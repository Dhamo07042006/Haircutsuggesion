# # utils/face_shape_model.py
# import torch
# import torch.nn as nn
# import torchvision.models as models

# class FaceShapeClassifier(nn.Module):
#     def __init__(self, num_classes=5):
#         super(FaceShapeClassifier, self).__init__()
#         self.backbone = models.mobilenet_v2(pretrained=False)
#         self.backbone.classifier[1] = nn.Linear(self.backbone.last_channel, num_classes)

#     def forward(self, x):
#         return self.backbone(x)

# def load_model(model_path):
#     model = FaceShapeClassifier(num_classes=5)
#     model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
#     model.eval()
#     return model

import torch
import torch.nn as nn
import torchvision.models as models

class FaceShapeClassifier(nn.Module):
    def __init__(self, num_classes=4):
        super(FaceShapeClassifier, self).__init__()
        self.backbone = models.mobilenet_v2(pretrained=False)
        self.backbone.classifier[1] = nn.Linear(self.backbone.last_channel, num_classes)

    def forward(self, x):
        return self.backbone(x)
