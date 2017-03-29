import requests
import socket
import logging


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        my_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                      'Accept-Language': 'zh-CN,zh;q=0.8'}
        try:
            response = requests.get(url, headers=my_headers, timeout=10)
        except requests.exceptions.ConnectionError as error:
            logging.warning('连接失败')
            logging.exception(error)
            return None
        except requests.packages.urllib3.exceptions.ReadTimeoutError as error:
            logging.warning('urllib3读取超时')
            logging.exception(error)
            return None
        except requests.exceptions.ReadTimeout:
            logging.warning('读取超时')
            return None
        except socket.timeout:
            logging.warning('超时')
            return None
        except Exception:
            logging.warning('未知错误')
            logging.exception(Exception)
            return None

        if response.status_code != requests.codes.ok:
            return None

        return response.content
