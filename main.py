from fastapi import FastAPI
from bs4 import BeautifulSoup
import aiohttp


async def get_site_content(link):
    hdr = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.107 Mobile Safari/537.36'}
    async with aiohttp.ClientSession() as session:
        async with session.get(link, headers=hdr) as resp:
            text = await resp.read()
    return text


async def wyr():
    url = 'https://either.io/'
    page_html = await get_site_content(url)

    page_soup = BeautifulSoup(page_html, "html.parser")
    questions = page_soup.find_all("span", {"class": "option-text"})
    percentage = page_soup.find_all("div", {"class": "percentage"})
    total = page_soup.find_all("div", {"class": "total-votes"})
    total_votes = page_soup.find_all("span", {"class": "contents"})
    ids = page_soup.find_all("div", {"class": "panel"})
    comments = page_soup.find_all("span", {"class": "comment-number"})
    desc = page_soup.find("p", {"class": "more-info"})
    return questions, percentage, total, ids[1]['data-question'], desc.text, total_votes[0].text, comments[0].text


app = FastAPI()


@app.get("/")
async def read_root():
    questions, percentage, total, ids, desc, total_votes, comments = await wyr()
    return {"id": ids, "description": desc, "comments": comments, "question1": questions[0].text,
            "question2": questions[1].text, "total-votes": total_votes, "BlueBoxAnswered": total[0].span.text,
            "RedBoxAnswered": total[1].span.text, "BluePercentage": percentage[0].text,
            "RedPercentage": percentage[1].text}

print(len("2275992109638223"))
