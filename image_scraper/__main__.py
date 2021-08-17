import os
import uuid
from uuid import uuid5
import logging
from importlib import import_module
from typing import Tuple

import fire
import requests
import pandas as pd
from bs4 import BeautifulSoup

from image_scraper.utils import delay_mean_and_std, check_if_visited_and_add
from image_scraper.config import default_config

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

def _download(config, url) -> Tuple[str, bytes]:
    try:
        if check_if_visited_and_add(url):
            logger.warn("url : {} is already visited.".format(url))
            return None
        r = requests.get(url, allow_redirects=True)
        delay_mean_and_std(config.DELAY_MEAN, config.DELAY_STD)
        return r.headers["content-type"], r.content
    except:
        logger.error("download error : {}".format(url))
        return None

def _save_image(config, url, content):
    try:
        if content:
            unq_id = str(uuid5(uuid.NAMESPACE_URL, name=url))
            filename = os.path.join(config.OUTPUT_DIR, unq_id + ".jpg")
            with open (filename, "wb") as f:
                f.write(content)
            logger.info("Saving {} as {}".format(url, unq_id))
            df = pd.DataFrame(data={"url" : [url], "uuid": [unq_id]}, columns=["url", "uuid"])
            df.to_csv(config.OUTPUT_DIR + "/" + config.META_FILE, index=False, header=False, mode="a")
    except:
        logger.error("error with url : {}".format(url))

def visit_page(config, page_url, cur_level=1):
    try:
        ctype, content = _download(config, url=page_url)
        if not content:
            return
        if ctype in config.IMAGE_TYPES:
            # store this image
            
            _save_image(config, url=page_url, content=content)
        elif ctype.startswith("text/html") and cur_level <= config.MAX_LEVEL: 
            soup = BeautifulSoup(content, 'html.parser')
            urls = config.get_urls(soup, url=page_url)
            for url in urls:
                visit_page(config, url, cur_level=cur_level + 1)
    except:
        logger.error("Unable to process {url}".format(url=page_url))

def _main(config):
    meta_file_path = os.path.join(config.OUTPUT_DIR, config.META_FILE)
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    if os.path.isfile(meta_file_path):
        df = pd.read_csv(meta_file_path, names=["url", "uuid"])
        _ = [check_if_visited_and_add(u) for u in df.url]
    else:
        df = pd.DataFrame(data={}, columns=["url", "uuid"])
        df.to_csv(meta_file_path, index=False, header=False, mode="a")
    for page_id in range(config.PAGE_START, config.PAGE_END + 1):
        logger.info("working on page_id : {}".format(page_id))
        page_url = config.URL_PREFIX.format(page_id=page_id)
        visit_page(config, page_url, cur_level=1)

def main(config_module:str=None):
    if not config_module:
        config_module = "image_scraper.config"
    path, obj = config_module.rsplit(".", 1)
    mod = import_module(path)
    config = getattr(mod, obj)
    _main(config=config)
    
if __name__ == "__main__":
    fire.Fire(main)