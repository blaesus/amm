import time
import json
import urllib.request

page = 1
pagesize = 100

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://civitai.com",
    "Referer": "https://civitai.com/",
}

while True:
    url = f'https://civitai.com/api/v1/models?page={page}&limit={pagesize}'
    print(f"Getting {url}")

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                if page >= 10000 or page > data['metadata']['totalPages']:
                    break
                with open(f'model-indices/{page}.json', 'w') as outfile:
                    json.dump(data, outfile, indent=4)
            else:
                print(f"Error: {response.status}")
    except urllib.error.HTTPError as e:
        print(f"Error: {e.code}")

    page += 1
    time.sleep(10)
