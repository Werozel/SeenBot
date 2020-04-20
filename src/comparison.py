from PIL import ImageChops, Image
import math
import requests
import time
from io import BytesIO


def rmsCompare(url1: str, raw) -> (float, str, ):
    # FIXME reques.get might be too long
    response1 = requests.get(url1)
    image1 = Image.open(BytesIO(response1.content))
    image2 = Image.open(BytesIO(raw))
    diff = ImageChops.difference(image1, image2)
    h = diff.histogram()
    sq = (value*((idx % 256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / float(image1.size[0] * image1.size[1]))
    return rms, url1

def rmsCompareRaw(raw1, raw2) -> (float, str, ):
    image1 = Image.open(BytesIO(raw1))
    image2 = Image.open(BytesIO(raw2))
    diff = ImageChops.difference(image1, image2)
    h = diff.histogram()
    sq = (value*((idx % 256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / float(image1.size[0] * image1.size[1]))
    return rms, ""
