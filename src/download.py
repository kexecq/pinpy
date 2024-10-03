from json import loads, dumps
from requests import get
from string import ascii_lowercase
from random import choice
from time import sleep
from log import log_out, log_err

"""
-   src/download.py
-   Author: @kexecq
-   Date: 30/09/2024
"""

def download(id: str):
    """This is the function that downloads the images.

    Args:
        id (int) The board id that we will be downloading images from.

    Returns:
        None
    """

    url = "https://www.pinterest.com/resource/BoardFeedResource/get/"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
    }
    params = {
        "source_url": "",
        "data": '{"options": {"board_id": "", "bookmarks": [null]}, "context": {}}',
    }

    """ Changes the board_id param to the one we grabbed. """
    change_id = loads(params["data"])
    change_id["options"]["board_id"] = str(id)
    params["data"] = dumps(change_id)

    """ Main loop for downloading images. """
    while True:
        r = get(url, headers=headers, params=params)
        req = r.json()

        """ Parsing the json response to look for image urls which we then download. """
        for urls in req["resource_response"]["data"]:
            if not urls.get("images"):
                break
            try:
                with open(''.join(choice(ascii_lowercase) 
                            for _ in range(10)) + '.jpg', "wb") as f:
                    f.write(get(urls["images"]["orig"]["url"]).content)
                    log_out("saved image!")
            except Exception as e:
                log_err(f"exception -> {e}")
            sleep(0.1)
    
        bookmark = req["resource_response"].get("bookmark")
        if bookmark is None:
            log_out("all images downloaded!")
            break

        """ Updating the 'bookmarks' value in our params with the new bookmark. """
        req_params = loads(params["data"])
        req_params["options"]["bookmarks"] = [bookmark]
        params["data"] = dumps(req_params)
        log_out("grabbed new bookmark, continuing.")
    
if __name__ == "__main__":
    download(input("[pinpy]: input board id: "))
