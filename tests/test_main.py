import pathlib
import threading
import glob
from tempfile import TemporaryDirectory
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from unittest import TestCase

from easydict import EasyDict as ed 

from image_scraper.__main__ import _main
from image_scraper.config import default_config

def _start_server(server:ThreadingHTTPServer):
    server.serve_forever(poll_interval=1)

THIS_FILE_PATH = pathlib.Path(__file__)
THIS_DIRECTORY = THIS_FILE_PATH.parent
SITE_DIRECTORY = pathlib.Path.joinpath(THIS_DIRECTORY, "sample-site")

OUTPUT_DIRECTORY = pathlib.Path.mkdir(pathlib.Path.joinpath(THIS_DIRECTORY, "outputs"), parents=True, exist_ok=True)

class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE_DIRECTORY, **kwargs)

server = ThreadingHTTPServer(
    server_address=("", 8080), RequestHandlerClass=(MyHandler)
)
t = threading.Thread(target=server.serve_forever, args=(1, ))

class TestSampleSite(TestCase):

    def setUp(self) -> None:
        t.start()
        super().setUp()
        
    def tearDown(self) -> None:
        server.shutdown()
        t.join()
        # self.p.join()
        super().tearDown()

    def test_all(self) -> None:
        with TemporaryDirectory() as output_dir:
            default_config.OUTPUT_DIR = output_dir
            default_config.DELAY_MEAN = 0.0
            default_config.DELAY_STD = 0.0
            _main(config=default_config)
            files = glob.glob(output_dir + "/*")
            assert len(files) == 10
