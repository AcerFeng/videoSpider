# !/usr/bin/nev python3
# coding:utf-8


from enum import Enum, unique
import data_handler
import html_downloader
import html_outputer
import html_parser
from models import RequestModel
import time


# 来源平台
@unique
class Platform(Enum):
    TengXunVideo = '腾讯视频'
    YouKuVido = '优酷视频'
    AiQiYi = '爱奇艺'

# 视频分类
@unique
class Video_category(Enum):
    Series = '电视剧'
    Movie = '电影'
    Variety = '综艺'

# 电视剧地区分类
@unique
class Series_region(Enum):
    All = '热播'
    Local = '内地'
    Net = '网剧'
    SouthKorea = '韩剧'
    EuropeAndAmerica = '欧美'

# 电影地区分类
@unique
class Movie_region(Enum):
    All = '热播'
    Cinemas = '院线'
    Local = '内地'
    HongKong = '港片'
    EuropeAndAmerica = '欧美'

# 综艺分类
@unique
class Variety_type(Enum):
    All = '热播'


@unique
class Craw_url(Enum):
    # 腾讯 电视剧 全部热播
    TX_Series_All_URL = 'http://v.qq.com/x/list/tv?offset=0&iyear=2017&sort=4&iarea=-1'
    TX_Series_Local_URL = 'http://v.qq.com/x/list/tv?iyear=2017&offset=0&iarea=814'
    TX_Series_Net_URL = 'http://v.qq.com/x/list/tv?offset=0&itype=844&iyear=2017'
    TX_Series_SouthKorea_URL = 'http://v.qq.com/x/list/tv?offset=0&iarea=818'
    TX_Series_EuropeAndAmerica_URL = 'http://v.qq.com/x/list/tv?offset=0&iarea=815'
    # 腾讯 电影
    TX_Movie_All_URL = 'http://v.qq.com/x/list/movie?offset=0&year=2017'
    TX_Movie_Cinemas_URL = 'http://v.qq.com/x/list/movie?year=2017&offset=0&subtype=100062'
    TX_Movie_Local_URL = 'http://v.qq.com/x/list/movie?offset=0&year=2017&area=100024'
    TX_Movie_HongKong_URL = 'http://v.qq.com/x/list/movie?area=100025&offset=0'
    TX_Movie_EuropeAndAmerica_URL = 'http://v.qq.com/x/list/movie?offset=0&area=100029&subtype=100062'
    # 腾讯 综艺
    TX_Variety_All_URL = 'http://v.qq.com/x/list/variety?offset=0'


INTERVAL = 5

class SpiderMain(object):
    def __init__(self):
        self.downloader = html_downloader.htmlDownloader()
        self.parser = html_parser.htmlParser()
        self.outputer = html_outputer.htmlOutPuter()
        self.data_handler = data_handler.DataHandler()

    def craw_tx_tv(self, url):
        print('crew tx tv...')
        try:
            html_cont = self.downloader.download(url)
            tx_video_datas = self.parser.parser_tx_video(url,html_cont)
            self.outputer.collect_data(tx_video_datas)
        except Exception:
            print('craw failed')
            raise Exception
        self.outputer.output_html()

    def start_craw(self, requestModel):
        if requestModel is None:
            return
        if requestModel.source_url is None:
            return
        if requestModel.platform is None:
            return
        if requestModel.video_category is None:
            return

        print('crawing:  %s:%s:%s' % (requestModel.source_url, requestModel.veriety_region, requestModel.video_category))
        # return
        if requestModel.platform == Platform.TengXunVideo:
            try:
                html_cont = self.downloader.download(requestModel.source_url.value)

                kw = {}
                if requestModel.series_region is not None:
                    kw['series_region'] = requestModel.series_region.value
                if requestModel.movie_region is not None:
                    kw['movie_region'] = requestModel.movie_region.value
                if requestModel.veriety_region is not None:
                    kw['veriety_region'] = requestModel.veriety_region.value

                crawed_datas = self.parser.parse_tx_video_data(requestModel.source_url, html_cont,
                                                               platform=requestModel.platform.value,
                                                               video_category=requestModel.video_category.value,
                                                               **kw
                                                               )
                if crawed_datas is None or len(crawed_datas) == 0:
                    print('not datas.')
                    return

                self.data_handler.save_data(crawed_datas)
                self.outputer.collect_data(crawed_datas)
            except Exception:
                print('craw tengxun video failed.')
                raise Exception

        elif requestModel.platform == Platform.AiQiYi:
            pass
        elif requestModel.platform == Platform.YouKuVido:
            pass
        else:
            print('not Found platform.')

# 抓取腾讯视频电视剧
def craw_tx_series(spider):
    requestModel1 = RequestModel(source_url=Craw_url.TX_Series_All_URL,
                                 platform=Platform.TengXunVideo,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.All)
    spider.start_craw(requestModel=requestModel1)
    time.sleep(INTERVAL)
    requestModel2 = RequestModel(source_url=Craw_url.TX_Series_Local_URL,
                                 platform=Platform.TengXunVideo,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.Local)
    spider.start_craw(requestModel=requestModel2)
    time.sleep(INTERVAL)
    requestModel3 = RequestModel(source_url=Craw_url.TX_Series_Net_URL,
                                 platform=Platform.TengXunVideo,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.Net)
    spider.start_craw(requestModel=requestModel3)
    time.sleep(INTERVAL)
    requestModel4 = RequestModel(source_url=Craw_url.TX_Series_SouthKorea_URL,
                                 platform=Platform.TengXunVideo,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.SouthKorea)
    spider.start_craw(requestModel=requestModel4)
    time.sleep(INTERVAL)
    requestModel5 = RequestModel(source_url=Craw_url.TX_Series_EuropeAndAmerica_URL,
                                 platform=Platform.TengXunVideo,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.EuropeAndAmerica)
    spider.start_craw(requestModel=requestModel5)

# 抓取腾讯视频电影
def craw_tx_movie(spider):
    requestModel1 = RequestModel(source_url=Craw_url.TX_Movie_All_URL,
                                 platform=Platform.TengXunVideo,
                                 video_category=Video_category.Movie,
                                 movie_region= Movie_region.All)
    spider.start_craw(requestModel=requestModel1)
    time.sleep(INTERVAL)
    requestModel2 = RequestModel(source_url=Craw_url.TX_Movie_Local_URL,
                                 platform=Platform.TengXunVideo,
                                 video_category=Video_category.Movie,
                                 movie_region=Movie_region.Local)
    spider.start_craw(requestModel=requestModel2)
    time.sleep(INTERVAL)
    requestModel3 = RequestModel(source_url=Craw_url.TX_Movie_Cinemas_URL,
                                 platform=Platform.TengXunVideo,
                                 video_category=Video_category.Movie,
                                 movie_region=Movie_region.Cinemas)
    spider.start_craw(requestModel=requestModel3)
    time.sleep(INTERVAL)
    requestModel4 = RequestModel(source_url=Craw_url.TX_Movie_HongKong_URL,
                                 platform=Platform.TengXunVideo,
                                 video_category=Video_category.Movie,
                                 movie_region=Movie_region.HongKong)
    spider.start_craw(requestModel=requestModel4)
    time.sleep(INTERVAL)
    requestModel5 = RequestModel(source_url=Craw_url.TX_Movie_EuropeAndAmerica_URL,
                                 platform=Platform.TengXunVideo,
                                 video_category=Video_category.Movie,
                                 movie_region=Movie_region.EuropeAndAmerica)
    spider.start_craw(requestModel=requestModel5)

# 抓取腾讯综艺
def craw_tx_variety(spider):
    requestModel1 = RequestModel(source_url=Craw_url.TX_Variety_All_URL,
                                 platform=Platform.TengXunVideo,
                                 video_category=Video_category.Variety,
                                 veriety_region=Variety_type.All)
    spider.start_craw(requestModel=requestModel1)

def craw_aiqiyi_series(spider):
    pass


if __name__ == '__main__':
    spider = SpiderMain()
    # craw_tx_series(spider)
    # time.sleep(5)
    # craw_tx_movie(spider)
    # time.sleep(5)
    craw_tx_variety(spider)