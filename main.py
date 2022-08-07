import base64
import os
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from image_classification.classifier import run_inference_on_image

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


class ImageProps(BaseModel):
    image: Union[str, bytes]
    num_top_predictions: int = 1


@app.post("/classify")
def classify(props: ImageProps):
    if isinstance(props.image, str):
        image = base64.b64decode(props.image)
    else:
        image = props.image

    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    print('CURRENT PATH: ' + current_dir_path)
    scores = run_inference_on_image(
        image, current_dir_path + '/image_classification/inception', props.num_top_predictions)
    return {"scores": scores}
