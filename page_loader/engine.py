from page_loader.get_data import get_data, get_response, get_content
from page_loader.process_data import process_data, download, create_path
from page_loader.save_data import save_data
import logging

logger = logging.getLogger()


def run_engine(args):
    storage = args.output
    source, url = get_data(args.url, get_response, get_content)
    local_source = process_data(source, url, storage, download, create_path)
    save_data(url, storage, local_source)
