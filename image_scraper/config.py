from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup
from easydict import EasyDict

# delay between calls (mean and standard deviation)
DELAY_MEAN = 4
DELAY_STD = 2

# random seed for delays
RANDOM_SEED = 123456

# url prefix with {page_id} placeholder
URL_PREFIX = "http://localhost:8080/page-{page_id}"
PAGE_START = 1
PAGE_END = 2

IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg"]

def get_urls(soup:BeautifulSoup, url=""):
    ahrefs = soup.find_all("a", href=True)
    urls = [urljoin(base=url, url=a["href"]) for a in ahrefs]
    urls = urls + [url + "/" + a["href"] for a in ahrefs if not url.endswith("/")]
    return urls

MAX_LEVEL=3

# output directory and meta file
OUTPUT_DIR = "~/outputs/"
META_FILE = "meta.csv"

_functions_to_include = [
    "get_urls", 
]

def dict_from_module(module):
    context = {}
    for k, v in module.items():
        if k.isupper() or k in _functions_to_include:
            context[k] = v
    return context

default_config = EasyDict(dict_from_module(globals()))
