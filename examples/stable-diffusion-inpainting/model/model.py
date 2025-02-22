from dataclasses import asdict
from typing import Dict

import torch
from base64_utils import b64_to_pil, pil_to_b64
from diffusers import StableDiffusionInpaintPipeline

STABLE_DIFFUSION_MODEL_ID = "runwayml/stable-diffusion-inpainting"


class Model:
    def __init__(self, **kwargs) -> None:
        self._model = None

    def load(self):
        self._model = StableDiffusionInpaintPipeline.from_pretrained(
            STABLE_DIFFUSION_MODEL_ID, revision="fp16", torch_dtype=torch.float16
        )
        self._model = self._model.to("cuda")

    def preprocess(self, request: Dict) -> Dict:
        # Convert from base64
        if "image" in request:
            request["image"] = b64_to_pil(request["image"])
        if "mask_image" in request:
            request["mask_image"] = b64_to_pil(request["mask_image"])
        return request

    def postprocess(self, request: Dict) -> Dict:
        # Convert to base64
        request.images = [pil_to_b64(img) for img in request.images]
        return asdict(request)

    def predict(self, request: Dict):
        response = self._model(**request)
        return response
