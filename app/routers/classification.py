# pylint: disable=import-error
"""Image classification API"""

import base64
import os
from typing import Union

from fastapi import APIRouter
from pydantic import BaseModel
from image_classification.classifier import run_inference_on_image

router = APIRouter()


class ImageProps(BaseModel):
    """Image classification model properties"""
    image: Union[str, bytes]
    num_top_predictions: int = 1


@router.post("/classify")
def classify(props: ImageProps):
    """Image classification endpoint"""
    if isinstance(props.image, str):
        image = base64.b64decode(props.image)
    else:
        image = props.image

    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    root_dir_path = os.path.abspath(os.path.join(
        os.path.join(current_dir_path, os.pardir), os.pardir))

    scores = run_inference_on_image(
        image, root_dir_path + '/image_classification/inception', props.num_top_predictions)

    return {"scores": scores}
