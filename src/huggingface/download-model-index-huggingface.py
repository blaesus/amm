import requests
import json
import re
from typing import Tuple

import time


# <https://huggingface.co/api/models?limit=%7B%7D&sort=downloads&cursor=eyIkb3IiOlt7ImRvd25sb2FkcyI6MCwiX2lkIjp7IiRndCI6IjYyNWZjMDYzZDQ3ZTNkYmFlMzJhNGM0OSJ9fSx7ImRvd25sb2FkcyI6eyIkZ3QiOjB9fSx7ImRvd25sb2FkcyI6bnVsbH1dfQ%3D%3D>; rel="next"
def parse_link_header(s: str) -> Tuple[str, str]:
    m = re.search('<(.*)>;.rel="(\w*)"', s)
    return (m.group(1), m.group(2))


page = 1
url = 'https://huggingface.co/api/models?limit=10000&full=true&sort=downloads&direction=-1'

while True:
    print("Getting {}".format(url))
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        with open('model-indices/{}.json'.format(page), 'w') as outfile:
            json.dump(data, outfile, indent=4)

    else:
        print(f"Error: {response.status_code}")

    (link, relation) = parse_link_header(response.headers["Link"])
    if relation == "next":
        url = link
    else:
        break

    page += 1
time.sleep(300)
