import requests
import socket

class htmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        my_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                      'Accept-Language':'zh-CN,zh;q=0.8'}
        try:
            response = requests.get(url, headers=my_headers, timeout=10)
        except requests.packages.urllib3.exceptions.ReadTimeoutError:
            print('连接超时')
            return None
        except requests.exceptions.ReadTimeout:
            print('读取超时')
            return None
        except socket.timeout:
            print('超时')
            return None
        except Exception:
            print('未知错误')
            raise Exception

        if response.status_code != requests.codes.ok:
            return None
        return response.content