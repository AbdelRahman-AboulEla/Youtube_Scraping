import pandas as pd
import json
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


######################################################################################################
def Bytes(size):
    items = ['Byte', 'KB', 'MB', 'GB', 'TB']
    for i in items:
        if size < 1024:
            return "%3.1f %s" % (size, i)
        size /= 1024


######################################################################################################
# open url
def execute_request(url, method=None, headers=None, data=None):
    base_headers = {"User-Agent": "Mozilla/5.0", "accept-language": "en-US,en"}
    if headers:
        base_headers.update(headers)
    request = Request(url, headers=base_headers, method=method, data=data)
    response = urlopen(request)
    return response


######################################################################################################
class Youtube:
    def __init__(self, url):
        self.url = url

    def All_videos(self):
        watch_html = execute_request(self.url).read().decode("utf-8")
        soup = BeautifulSoup(watch_html, "html.parser")
        body = soup.find_all("body", dir="ltr")[0]
        li = len('var ytInitialPlayerResponse = ')
        script = body.find_all("script")[0].string[li:-1]
        results = json.loads(script)
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


if __name__ == '__main__':
    link = input('Please inter url: ')
    videos = Youtube(link)
    print(videos.stream())
    ind = int(input('Please select index: '))
    print(videos.link()[ind])
    input('Press Enter to close')
