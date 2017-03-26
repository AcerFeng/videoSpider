# !/usr/bin/nev python3
# coding:utf-8
import html_downloader
import html_outputer
import html_parser

TX_HOT_TV_URL = "http://v.qq.com/x/list/tv?offset=0&iyear=2017&sort=4&iarea=-1"
TX_MOVIE_URL = "http://v.qq.com/movie/"


class SpiderMain(object):
    def __init__(self):
        self.downloader = html_downloader.htmlDownloader()
        self.parser = html_parser.htmlParser()
        self.outputer = html_outputer.htmlOutPuter()

    def craw_tx_tv(self, url):
        print('crew tx tv...')
        try:
            html_cont = self.downloader.download(url)
            tx_tv_data = self.parser.parser_tx_tv(url,html_cont)
            self.outputer.collect_data(tx_tv_data)
        except Exception:
            print('craw failed')
            raise Exception
        self.outputer.output_html()


if __name__ == '__main__':
    spider = SpiderMain()
    spider.craw_tx_tv(TX_HOT_TV_URL)
    