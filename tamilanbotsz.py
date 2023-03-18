import requests

import pyshorteners
from info import SHORTNER_SITE, SHORTNER_API

def short_url(longurl):
    if "shorte.st" in SHORTNER_SITE:
        disable_warnings()
        return requests.get(f'http://api.shorte.st/stxt/{SHORTNER_API}/{longurl}', verify=False).text
    elif "linkvertise" in SHORTNER_SITE:
        url = quote(base64.b64encode(longurl.encode("utf-8")))
        linkvertise = [
            f"https://link-to.net/{SHORTNER_API}/{random.random() * 1000}/dynamic?r={url}",
            f"https://up-to-down.net/{SHORTNER_API}/{random.random() * 1000}/dynamic?r={url}",
            f"https://direct-link.net/{SHORTNER_API}/{random.random() * 1000}/dynamic?r={url}",
            f"https://file-link.net/{SHORTNER_API}/{random.random() * 1000}/dynamic?r={url}"]
        return random.choice(linkvertise)
    elif "bitly.com" in SHORTNER_SITE:
        s = pyshorteners.Shortener(api_key=SHORTNER_API)
        return s.bitly.short(longurl)
    elif "ouo.io" in SHORTNER_SITE:
        disable_warnings()
        return requests.get(f'http://ouo.io/api/{SHORTNER_API}?s={longurl}', verify=False).text
    else:
        return requests.get(f'https://{SHORTNER_SITE}/api?api={SHORTNER_API}&url={longurl}&format=text').text
