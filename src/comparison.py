from PIL import ImageChops, Image
import math
import requests
import time
from io import BytesIO


# Returns bool and link to similar picture
def check_bayan(url: str, size: str, urls: dict) -> dict:
    if urls.get(size) is None:
        print("No such size, returning...", flush=True)
        return {"url": url, "result": False, "simlink": None, "size": size}
    for url_list in list(urls.values()):
        if url in list(url_list.keys()):
            print("Same link", flush=True)
            return {"url": url, "result": True, "simlink": url, "size": size}
    # results = [pool.apply_async(rmsCompare, args=(i, url,)) for i in list(urls.get(size).keys())]
    results = [rmsCompare(i, url) for i in list(urls.get(size).keys())]
    for res, s in results:
        if res < 10:
            print("bayan, has similar picture", flush=True)
            return {"url": url, "result": True, "simlink": s, "size": size}
    print("not bayan, returning...", flush=True)
    return {"url": url, "result": False, "simlink": None, "size": size}


def rmsCompare(url1: str, url2: str) -> (float, str, ):
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    image1 = Image.open(BytesIO(response1.content))
    image2 = Image.open(BytesIO(response2.content))
    diff = ImageChops.difference(image1, image2)
    h = diff.histogram()
    sq = (value*((idx % 256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / float(image1.size[0] * image1.size[1]))
    return rms, url1