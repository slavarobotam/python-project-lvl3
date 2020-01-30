from page_loader.fetching import fetch_data, get_content, get_response
from page_loader.processing import download, normalize, process_data
from page_loader.storing import save_data


def run_engine(args):
    try:
        source, url = fetch_data(args.url, get_response, get_content)
        local_source = process_data(source, url, args.output, download,
                                    normalize)
        save_data(url, args.output, local_source)
    except Exception:
        return False
    else:
        return True
