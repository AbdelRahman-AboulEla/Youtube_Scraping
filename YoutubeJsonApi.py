import json
from urllib import parse
from urllib.request import Request, urlopen
import requests
import pandas as pd

base_params = {'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8', 'contentCheckOk': True, 'racyCheckOk': True}
base_data = {'context': {'client': {'clientName': 'ANDROID', 'clientVersion': '16.20'}}}


def Bytes(size):
    items = ['Byte', 'KB', 'MB', 'GB', 'TB']
    for i in items:
        if size < 1024:
            return "%3.1f %s" % (size, i)
        size /= 1024


def execute_request(url, method=None, headers=None, data=None):
    base_headers = {"User-Agent": "Mozilla/5.0", "accept-language": "en-US,en"}
    if headers:
        base_headers.update(headers)
    if data:
        if not isinstance(data, bytes):
            data = bytes(json.dumps(data), encoding="utf-8")
    if url.lower().startswith("http"):
        request = Request(url, headers=base_headers, method=method, data=data)
    else:
        raise ValueError("Invalid URL")
    return urlopen(request)


def VideoID(url):
    return parse.urlparse(url).query[2:]


def JsonContent(url):
    endpoint = f'https://www.youtube.com/youtubei/v1/player'
    query = {'videoId': VideoID(url), }
    query.update(base_params)
    endpoint_url = f'{endpoint}?{parse.urlencode(query)}'
    headers = {'Content-Type': 'application/json', }
    response = execute_request(endpoint_url, 'POST', headers=headers, data=base_data)
    return json.loads(response.read())


class Youtube:
    def __init__(self, url):
        self.url = url

    def All_videos(self):
        results = JsonContent(self.url)
        video1 = results['streamingData']['formats']
        video2 = results['streamingData']['adaptiveFormats']
        return video1 + video2

    def link(self):
        url = []
        for i in self.All_videos():
            try:
                url.append(i["url"])
            except:
                url.append("")
        return url

    def mimeType(self):
        mimeType = []
        for i in self.All_videos():
            try:
                mimeType.append(i["mimeType"].split(';')[0])
            except:
                mimeType.append("")
        return mimeType

    def codecs(self):
        mimeType = []
        for i in self.All_videos():
            try:
                mimeType.append(i["mimeType"].split(';')[1])
            except:
                mimeType.append("")
        return mimeType

    def contentLength(self):
        contentLength = []
        for i in self.All_videos():
            try:
                x = i["contentLength"]
                x = Bytes(int(x))
                contentLength.append(x)
            except:
                # x = int(i["approxDurationMs"]) * int(i["bitrate"]) / 8000
                # x = Bytes(int(x))
                contentLength.append('x')
        return contentLength

    def qualityLabel(self):
        qualityLabel = []
        for i in self.All_videos():
            try:
                qualityLabel.append(i["qualityLabel"])
            except:
                qualityLabel.append("")
        return qualityLabel

    def quality(self):
        quality = []
        for i in self.All_videos():
            try:
                quality.append(i["quality"])
            except:
                quality.append("")
        return quality

    def stream(self):
        return pd.DataFrame({'type': self.mimeType(),
                             'codecs': self.codecs(),
                             'quality': self.qualityLabel(),
                             'Size': self.contentLength(),
                             'qu': self.quality()
                             })


urll = input('Please inter url: ')
v = Youtube(urll)
print(v.stream())
ind = int(input('Please select index: '))
print(v.link()[ind])
input('Press Enter to Colse')