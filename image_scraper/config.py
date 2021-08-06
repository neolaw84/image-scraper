from easydict import EasyDict

# delay between calls (mean and standard deviation)
DELAY_MEAN = 4
DELAY_STD = 2

# random seed for delays
RANDOM_SEED = 123456

# url prefix with {page_id} placeholder
URL_PREFIX = "https://www.example-galleries.com/{page_id}"
PAGE_START = 1
PAGE_END = 99
# all a href within this class will be followed
PAGE_DIV_CLASS = "div_with_links"
PAGE_COMPONENT=None

# a function to extract links from a href
# return None to stop following
def extract_link(ahref:str=None):
    try:
        return ahref
    except:
        return None

SUB_PAGE_DIV_CLASS = "div_more_sub_pages"
SUB_PAGE_START = 1
# SUB_PAGE_END will be based on the a href with "Last" as body
# SUB_PAGE_END = #

# a function to extract links from a href in sub-pages
# return None to stop following
def extract_link_sub_page(ahref:str=None):
    return extract_link(ahref)

def get_siblings(component):
    try:
        hrefs = component.find_all("a", href=True)
        return [h["href"] for h in hrefs]
    except:
        return []

def get_image_url(component):
    try:
        url = component["href"]
        if url.endswith("jpg") or url.endswith("png") or url.endswith("jpeg"):
            return url
    except:
        return None

# output directory and meta file
OUTPUT_DIR = "~/outputs/"
META_FILE = "meta.csv"

NESTED_TRY = False

_functions_to_include = [
    "extract_link", 
    "extract_link_sub_page", 
    "get_siblings", 
    "get_image_url", 
]

def dict_from_module(module):
    context = {}
    for k, v in module.items():
        if k.isupper() or k in _functions_to_include:
            context[k] = v
    return context

default_config = EasyDict(dict_from_module(globals()))
