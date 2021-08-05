import os
import uuid
from uuid import uuid5
import logging

import requests
import pandas as pd
from bs4 import BeautifulSoup

from image_scraper.utils import delay_mean_and_std

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

def _download(config, url):
    try:
        r = requests.get(url, allow_redirects=True)
        delay_mean_and_std(config.DELAY_MEAN, config.DELAY_STD)
        return r.content
    except:
        return None

def visit_image(config, url):
    try:
        content = _download(config, url)
        if content:
            unq_id = str(uuid5(uuid.NAMESPACE_URL, name=url))
            filename = os.path.join(config.OUTPUT_DIR, unq_id + ".jpg")
            with open (filename, "wb") as f:
                f.write(content)
            df = pd.DataFrame(data={"url" : [url], "uuid": [unq_id]}, columns=["url", "uuid"])
            df.to_csv(config.OUTPUT_DIR + "/" + config.META_FILE, index=False, header=True, mode="a")
    except:
        logger.error("error with url : {}".format(url))

def visit_model_page(config, url):
    content = _download(config, url)
    if not content:
        return
    soup = BeautifulSoup(content, "html.parser")
    divs = soup.find_all("div", {"class": config.PAGE_DIV_CLASS})
    for div in divs:
        hrefs = div.find_all("a", href=True)
        for h in hrefs:
            u = config.get_image_url(h)
            if u:
                visit_image(config, url=u)

def visit_model_pages(config, url):
    content = _download(config, url)
    if not content:
        return
    soup = BeautifulSoup(content, "html.parser")
    urls = config.get_siblings(soup)
    if urls:
        for u in urls:
            visit_model_page(config, u)
    else:
        visit_model_page(config, url)

def visit_page(config, page_url):
    def _extract_a_href(page_div):
        hrefs = page_div.find_all(href=True)
        for href in hrefs:
            link = config.extract_link(ahref=href["href"])
            if link:
                visit_model_pages(config, link)
    try:
        content = _download(config, url=page_url)
        if not content:
            return
        soup = BeautifulSoup(content, 'html.parser')
        page_div = soup.find_all("div", {"class":config.PAGE_DIV_CLASS})
        if isinstance(page_div, list):
            for pd in page_div:
                _extract_a_href(pd)
        else:
            _extract_a_href(page_div)
    except:
        logger.error("Unable to process {url}".format(url=page_url))

def main(config):
    df = pd.DataFrame(data={}, columns=["url", "uuid"])
    df.to_csv(config.OUTPUT_DIR + "/" + config.META_FILE, index=False, header=False, mode="a")
    for page_id in range(config.PAGE_START, config.PAGE_END + 1):
        page_url = config.URL_PREFIX.format(page_id=page_id)
        visit_page(config, page_url)

