import random

import requests
from fastapi import FastAPI
from starlette.responses import HTMLResponse

app = FastAPI()

@app.get("/flags")
def get_flags():
    d = get_country_flag_urls()
    if d:
        html_content = ""
        country, flag_url = random.choice(list(d.items()))
        flag_url = flag_url.replace('50px', '1000px')
        image_tag = f'<img src="{flag_url}" alt="Flag">'
        html_content += image_tag
        return HTMLResponse(content=html_content, media_type="text/html")
    else:
        return {"message": "Failed to retrieve flag URLs"}
def get_country_flag_urls():
    url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2"

    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content to extract the flag URLs using BeautifulSoup
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        flag_urls = {}
        table = soup.find('table', class_='wikitable')
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 2:
                country = columns[0].text.strip()
                flag_url = columns[1].find('img')['src']
                flag_urls[country] = flag_url
        return flag_urls
    else:
        # Handle the case when the request fails
        return None
