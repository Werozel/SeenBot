from PIL import ImageChops, Image
import math
import requests
from io import BytesIO

from libs.PictureSize import PictureSize


def rms_compare(pic: PictureSize, raw_pic) -> (float, str,):
    pic_url: str = pic.link
    response1 = requests.get(pic_url)
    image1 = Image.open(BytesIO(response1.content))
    image2 = Image.open(BytesIO(raw_pic))
    diff = ImageChops.difference(image1, image2)
    h = diff.histogram()
    sq = (value*((idx % 256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / float(image1.size[0] * image1.size[1]))
    return rms, pic


def rms_compare_raw(raw1, raw2) -> (float, str,):
    image1 = Image.open(BytesIO(raw1))
    image2 = Image.open(BytesIO(raw2))
    diff = ImageChops.difference(image1, image2)
    h = diff.histogram()
    sq = (value*((idx % 256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / float(image1.size[0] * image1.size[1]))
    return rms, ""
