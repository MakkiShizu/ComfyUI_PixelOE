from pixeloe.pixelize import pixelize

import cv2
import torch
import numpy as np

class PixelOE:
    mode=["center","contrast","k-centroid","bicubic","nearest"]

    @staticmethod
    def tensor2opencv(image):
        return cv2.cvtColor(
            np.clip(255.0 * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8),
            cv2.COLOR_RGB2BGR
        )

    @staticmethod
    def opencv2tensor(image):
        return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mode": (cls.mode, {"default": "contrast"}),
                "target_size": ("INT", {"default": 128, "min": 0, "max": 1024, "step": 1}),
                "patch_size": ("INT", {"default": 16, "min": 0, "max": 64, "step": 1}),
                "thickness": ("INT", {"default": 2, "min": 0, "max": 16, "step": 1}),
                "color_matching": ("BOOLEAN", {"default": True}),
                "contrast": ("FLOAT", {"default": 1, "min": 0, "max": 10, "step": 0.1}),
                "saturation": ("FLOAT", {"default": 1, "min": 0, "max": 10, "step": 0.1}),
                "colors": ("BOOLEAN", {"default": False}),
                "colors_num": ("INT", {"default": 32, "min": 1, "max": 255, "step": 1}),
                "no_upscale": ("BOOLEAN", {"default": False}),
                "no_downscale": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "PixelOE"
    CATEGORY = "image"

    def PixelOE(self, image, mode, target_size, patch_size, thickness, color_matching, contrast, saturation, colors, colors_num, no_upscale, no_downscale):
        cv2_img = self.tensor2opencv(image)

        if colors == False:
            colors = None
        if colors == True:
            colors = colors_num

        print(mode, target_size, patch_size, thickness, color_matching, contrast, saturation, colors, no_upscale, no_downscale)

        img = pixelize(cv2_img, mode, target_size, patch_size, thickness, color_matching, contrast, saturation, colors, no_upscale, no_downscale)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        return (self.opencv2tensor(img_rgb),)

NODE_CLASS_MAPPINGS = {"PixelOE": PixelOE}
NODE_DISPLAY_NAME_MAPPINGS = {"PixelOE": "PixelOE"}
