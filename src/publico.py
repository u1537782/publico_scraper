from bs4 import BeautifulSoup
import json
from pathlib import Path
import requests

OUTPUT_PATH = Path("data/publico")
OUTPUT_PATH.mkdir(exist_ok=True, parents=True)


def get_text(url: str) -> str:
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    text_element = soup.find(name="div", id="story-body")
    text = "\n".join(p_element.text for p_element in text_element.find_all("p"))
    return text


if __name__ == "__main__":

    max_id = 3_000_000
    for news_id in range(995_915, max_id):
        print(f"Working in id {news_id}/{max_id}")
        url = f'https://www.publico.pt/api/content/news/{news_id}'

        try:
            response = requests.get(url, timeout=10)
        except:
            print(f"Did not get a response from url {url}")
            continue

        if response.status_code == 200:
            print("\tFound content.")
            content = response.json()
            news_url = content["shareUrl"]

            try:
                text = get_text(news_url)
            except:
                print(f"\tWas not able to extract text from {news_url}.")
                continue

            content["texto"] = text

            with open(OUTPUT_PATH / f"{news_id}.json", "w") as fout:
                json.dump(content, fout, indent=4)
