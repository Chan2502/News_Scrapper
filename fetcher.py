import time
import requests


def fetcher(query, page_no):
    url = "https://search.prod.di.api.cnn.io/content"
    querystring = {
        "q": query,
        "size": "10",
        "from": str((page_no - 1) * 10),
        "page": str(page_no),
        "sort": "newest",
        "request_id": "pdx-search-a429b049-b067-4cb9-856e-e0ffb40c6607"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://edition.cnn.com/",
        "Origin": "https://edition.cnn.com",
        "DNT": "1",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "TE": "trailers"
    }
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for page {page_no}")
        return None


query = "accident"
lastindex = 1

for page_no in range(1, 6):
    NewsJson = fetcher(query, page_no)
    if NewsJson is None:
        continue

    results = NewsJson.get('result', [])
    subtractor = 0

    for index, result in enumerate(results, lastindex):
        if not result.get('body', '').strip():
            subtractor += 1
            continue
        print(f"{index - subtractor}. {result['body']}")
        lastindex = index - subtractor

    time.sleep(3)  # to bypass bot detection
