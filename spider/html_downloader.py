from urllib import request


class htmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        req = request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
        response = request.urlopen(req)
        if response.getcode() != 200:
            return None
        return response.read()