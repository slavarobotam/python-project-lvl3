from page_loader.get_data import get_data
from page_loader.process_data import process_data
from page_loader.save_data import save_data
from page_loader.logging import run_logging


def engine(args):
    run_logging(args)
    page_source, url = get_data(args.url)
    local_page_source = process_data(page_source, url, args.output)
    save_data(url, args.output, local_page_source)
