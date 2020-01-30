import logging

from page_loader.get_data import get_content, get_data, get_response
from page_loader.process_data import create_path, download, process_data
from page_loader.save_data import save_data

logger = logging.getLogger()


def run_engine(args):
    try:
        source, url = get_data(args.url, get_response, get_content)
        local_source = process_data(source, url, args.output, download,
                                    create_path)
        save_data(url, args.output, local_source)
    except Exception:
        return False
    else:
        return True
