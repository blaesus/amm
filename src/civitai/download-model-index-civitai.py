import requests
import json

page = 40
pagesize=100

while True:
    url = 'https://civitai.com/api/v1/models?page={}&limit={}'.format(page, pagesize)
    print("Getting {}".format(url))
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        if page >= 10000 or page > data['metadata']['totalPages']:
            break
        with open('model-indices/{}.json'.format(page), 'w') as outfile:
            json.dump(data, outfile, indent=4)
    else:
        print(f"Error: {response.status_code}")

    page += 1
