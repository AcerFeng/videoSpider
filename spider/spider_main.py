# !/usr/bin/nev python3
# coding:utf-8


from enum import Enum, unique
import data_handler
import html_downloader
import html_outputer
import html_parser
from models import RequestModel
import time
import logging.config
import os
import yaml


# 来源平台
@unique
class Platform(Enum):
    TengXunVideo = '腾讯视频'
    YouKuVido = '优酷视频'
    AiQiYi = '爱奇艺'


# 视频分类
@unique
class VideoCategory(Enum):
    Series = '电视剧'
    Movie = '电影'
    Variety = '综艺'


# 电视剧地区分类
@unique
class SeriesRegion(Enum):
    All = '热播'
    Local = '内地'
    Net = '网剧'
    SouthKorea = '韩剧'
    America = '美国'


# 电影地区分类
@unique
class MovieRegion(Enum):
    All = '热播'
    Cinemas = '院线'
    Chines = '华语'
    Local = '内地'
    HongKong = '港片'
    America = '美国'


# 综艺分类
@unique
class VarietyType(Enum):
    All = '热播'


@unique
class CrawURL(Enum):
    # 腾讯 电视剧 全部热播
    TX_Series_All_URL = 'http://www.google.com'
    TX_Series_Local_URL = 'http://v.qq.com/x/list/tv?iyear=2017&offset=0&iarea=814'
    TX_Series_Net_URL = 'http://v.qq.com/x/list/tv?offset=0&itype=844&iyear=2017'
    TX_Series_SouthKorea_URL = 'http://v.qq.com/x/list/tv?offset=0&iarea=818'
    TX_Series_America_URL = 'http://v.qq.com/x/list/tv?offset=0&iarea=815'
    # 腾讯 电影
    TX_Movie_All_URL = 'http://v.qq.com/x/list/movie?offset=0&year=2017'
    TX_Movie_Cinemas_URL = 'http://v.qq.com/x/list/movie?year=2017&offset=0&subtype=100062'
    TX_Movie_Local_URL = 'http://v.qq.com/x/list/movie?offset=0&year=2017&area=100024'
    TX_Movie_HongKong_URL = 'http://v.qq.com/x/list/movie?area=100025&offset=0'
    TX_Movie_America_URL = 'http://v.qq.com/x/list/movie?offset=0&area=100029&subtype=100062'
    # 腾讯 综艺
    TX_Variety_All_URL = 'http://v.qq.com/x/list/variety?offset=0'

    # 爱奇艺 电视剧
    AiQiYi_Series_All_URL = 'http://list.iqiyi.com/www/2/----------------iqiyi--.html'
    AiQiYi_Series_Local_URL = 'http://list.iqiyi.com/www/2/15-------------11-1-1-iqiyi--.html'
    AiQiYi_Series_Net_URL = 'http://list.iqiyi.com/www/2/-11992------------11-1-1-iqiyi--.html'
    AiQiYi_Series_SouthKorea_URL = 'http://list.iqiyi.com/www/2/17-------------11-1-1-iqiyi--.html'
    AiQiYi_Series_America_URL = 'http://list.iqiyi.com/www/2/18-------------11-1-1-iqiyi--.html'
    # 爱奇艺 电影
    AiQiYi_Movie_All_URL = 'http://list.iqiyi.com/www/1/----------------iqiyi--.html'
    AiQiYi_Movie_Cinemas_URL = 'http://list.iqiyi.com/www/1/------27815-----2017--11-1-1-iqiyi--.html'
    AiQiYi_Movie_Chines_URL = 'http://list.iqiyi.com/www/1/1-----------2017--11-1-1-iqiyi--.html'
    AiQiYi_Movie_America_URL = 'http://list.iqiyi.com/www/1/2-------------11-1-1-iqiyi--.html'
    # 爱奇艺 综艺
    AiQiYi_Variety_All_URL = 'http://list.iqiyi.com/www/6/----------------iqiyi--.html'

    # 优酷 电视剧
    YouKu_Series_All_URL = 'http://list.youku.com/category/show/c_97_r__s_1_d_1.html?spm=a2h1n.8251845.filterPanel.5!4~1~3~A'
    YouKu_Series_Local_URL = 'http://list.youku.com/category/show/c_97_s_1_d_1_a_%E5%A4%A7%E9%99%86.html?spm=a2h1n.8251845.filterPanel.5!2~1~3!2~A'
    YouKu_Series_Net_URL = 'http://list.youku.com/category/show/c_97_s_1_d_1_g_%E4%BC%98%E9%85%B7%E5%87%BA%E5%93%81.html?spm=a2h1n.8251845.filterPanel.5!3~1~3!18~A'
    YouKu_Series_SouthKorea_URL = 'http://list.youku.com/category/show/c_97_a_%E9%9F%A9%E5%9B%BD_r__s_1_d_1.html?spm=a2h1n.8251845.filterPanel.5!4~1~3~A'
    YouKu_Series_America_URL = 'http://list.youku.com/category/show/c_97_a_%E7%BE%8E%E5%9B%BD_r__s_1_d_1.html?spm=a2h1n.8251845.filterPanel.5!4~1~3~A'
    # 优酷 电影
    YouKu_Movie_All_URL = 'http://list.youku.com/category/show/c_96_r__s_1_d_1.html?spm=a2h1n.8251845.filterPanel.5!4~1~3~A'
    YouKu_Movie_Local_URL = 'http://list.youku.com/category/show/c_96_s_1_d_1_a_%E5%A4%A7%E9%99%86.html?spm=a2h1n.8251845.filterPanel.5!2~1~3!2~A'
    YouKu_Movie_HongKong_URL = 'http://list.youku.com/category/show/c_96_a_%E9%A6%99%E6%B8%AF_s_1_d_1.html?spm=a2h1n.8251845.filterPanel.5!2~1~3!3~A'
    YouKu_Movie_America_URL = 'http://list.youku.com/category/show/c_96_a_%E7%BE%8E%E5%9B%BD_s_1_d_1.html?spm=a2h1n.8251845.filterPanel.5!2~1~3!7~A'
    # 优酷 综艺
    YouKu_Variety_All_URL = 'http://list.youku.com/category/show/c_85_s_1_d_1_r_2017.html?spm=a2h1n.8251845.filterPanel.5!4~1~3!2~A'


INTERVAL = 20


class SpiderMain(object):
    def __init__(self):
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutPuter()
        self.data_handler = data_handler.DataHandler()

    def start_craw(self, request_model):
        if request_model is None:
            return
        if request_model.source_url is None:
            return
        if request_model.platform is None:
            return
        if request_model.video_category is None:
            return

        logging.info('fetching:  %s:%s:%s:%s' % (request_model.platform.value,
                                                 request_model.video_category.value,
                                                 request_model.source_url,
                                                 request_model.source_url.value))

        html_cont = self.downloader.download(request_model.source_url.value)
        if html_cont is None:
            logging.info('download fail.')
            return
        logging.info('download success.')

        kw = {}
        if request_model.series_region is not None:
            kw['series_region'] = request_model.series_region.value
        if request_model.movie_region is not None:
            kw['movie_region'] = request_model.movie_region.value
        if request_model.veriety_region is not None:
            kw['veriety_region'] = request_model.veriety_region.value

        crawed_datas = []
        if request_model.platform == Platform.TengXunVideo:
            try:
                crawed_datas = self.parser.parse_tx_video_data(request_model.source_url, html_cont,
                                                               platform=request_model.platform.value,
                                                               video_category=request_model.video_category.value,
                                                               **kw
                                                               )
            except Exception:
                logging.warning('parse %s:%s:%s failed.' % (request_model.platform.value,
                                                            request_model.video_category.value,
                                                            request_model.source_url.value))
                raise Exception

        elif request_model.platform == Platform.AiQiYi:
            try:
                crawed_datas = self.parser.parse_aiqiyi_video_data(request_model.source_url,
                                                                   html_cont,
                                                                   platform=request_model.platform.value,
                                                                   video_category=request_model.video_category.value,
                                                                   **kw)
            except Exception:
                logging.warning('parse %s:%s:%s failed.' % (request_model.platform.value,
                                                            request_model.video_category.value,
                                                            request_model.source_url.value))
                raise Exception

        elif request_model.platform == Platform.YouKuVido:
            try:
                crawed_datas = self.parser.parse_youku_video_data(request_model.source_url,
                                                                  html_cont,
                                                                  platform=request_model.platform.value,
                                                                  video_category=request_model.video_category.value,
                                                                  **kw)

            except Exception:
                logging.warning('parse %s:%s:%s failed.' % (request_model.platform.value,
                                                            request_model.video_category.value,
                                                            request_model.source_url.value))
                raise Exception
        else:
            logging.info('not Found platform.')

        if len(crawed_datas) == 0:
            logging.info('not found %s datas.' % request_model.platform.value)
            return
        logging.info('craw success!')
        # self.data_handler.save_data(crawed_datas)
        # self.outputer.collect_data(crawed_datas)


# 抓取腾讯视频电视剧
def craw_tx_series(spider):
    request_model1 = RequestModel(source_url=CrawURL.TX_Series_All_URL,
                                  platform=Platform.TengXunVideo,
                                  video_category=VideoCategory.Series,
                                  series_region=SeriesRegion.All)
    spider.start_craw(request_model=request_model1)
    time.sleep(INTERVAL)
    request_model2 = RequestModel(source_url=CrawURL.TX_Series_Local_URL,
                                  platform=Platform.TengXunVideo,
                                  video_category=VideoCategory.Series,
                                  series_region=SeriesRegion.Local)
    spider.start_craw(request_model=request_model2)
    time.sleep(INTERVAL)
    request_model3 = RequestModel(source_url=CrawURL.TX_Series_Net_URL,
                                  platform=Platform.TengXunVideo,
                                  video_category=VideoCategory.Series,
                                  series_region=SeriesRegion.Net)
    spider.start_craw(request_model=request_model3)
    time.sleep(INTERVAL)
    request_model4 = RequestModel(source_url=CrawURL.TX_Series_SouthKorea_URL,
                                  platform=Platform.TengXunVideo,
                                  video_category=VideoCategory.Series,
                                  series_region=SeriesRegion.SouthKorea)
    spider.start_craw(request_model=request_model4)
    time.sleep(INTERVAL)
    request_model5 = RequestModel(source_url=CrawURL.TX_Series_America_URL,
                                  platform=Platform.TengXunVideo,
                                  video_category=VideoCategory.Series,
                                  series_region=SeriesRegion.America)
    spider.start_craw(request_model=request_model5)

# 抓取腾讯视频电影
def craw_tx_movie(spider):
    request_model1 = RequestModel(source_url=CrawURL.TX_Movie_All_URL,
                                  platform=Platform.TengXunVideo,
                                  video_category=VideoCategory.Movie,
                                  movie_region= MovieRegion.All)
    spider.start_craw(request_model=request_model1)
    time.sleep(INTERVAL)
    request_model2 = RequestModel(source_url=CrawURL.TX_Movie_Local_URL,
                                  platform=Platform.TengXunVideo,
                                  video_category=VideoCategory.Movie,
                                  movie_region=MovieRegion.Local)
    spider.start_craw(request_model=request_model2)
    time.sleep(INTERVAL)
    request_model3 = RequestModel(source_url=CrawURL.TX_Movie_Cinemas_URL,
                                  platform=Platform.TengXunVideo,
                                  video_category=VideoCategory.Movie,
                                  movie_region=MovieRegion.Cinemas)
    spider.start_craw(request_model=request_model3)
    time.sleep(INTERVAL)
    request_model4 = RequestModel(source_url=CrawURL.TX_Movie_HongKong_URL,
                                  platform=Platform.TengXunVideo,
                                  video_category=VideoCategory.Movie,
                                  movie_region=MovieRegion.HongKong)
    spider.start_craw(request_model=request_model4)
    time.sleep(INTERVAL)
    request_model5 = RequestModel(source_url=CrawURL.TX_Movie_America_URL,
                                  platform=Platform.TengXunVideo,
                                  video_category=VideoCategory.Movie,
                                  movie_region=MovieRegion.America)
    spider.start_craw(request_model=request_model5)


# 抓取腾讯综艺
def craw_tx_variety(spider):
    request_model1 = RequestModel(source_url=CrawURL.TX_Variety_All_URL,
                                  platform=Platform.TengXunVideo,
                                  video_category=VideoCategory.Variety,
                                  veriety_region=VarietyType.All)
    spider.start_craw(request_model=request_model1)


# 爱奇艺电视剧
def craw_aiqiyi_series(spider):
    request_model1 = RequestModel(source_url=CrawURL.AiQiYi_Series_All_URL,
                                  platform=Platform.AiQiYi,
                                  video_category=VideoCategory.Series,
                                  series_region=SeriesRegion.All)
    spider.start_craw(request_model=request_model1)
    time.sleep(INTERVAL)
    request_model2 = RequestModel(source_url=CrawURL.AiQiYi_Series_Local_URL,
                                  platform=Platform.AiQiYi,
                                  video_category=VideoCategory.Series,
                                  series_region=SeriesRegion.Local)
    spider.start_craw(request_model=request_model2)
    time.sleep(INTERVAL)
    request_model3 = RequestModel(source_url=CrawURL.AiQiYi_Series_Net_URL,
                                  platform=Platform.AiQiYi,
                                  video_category=VideoCategory.Series,
                                  series_region=SeriesRegion.Net)
    spider.start_craw(request_model=request_model3)
    time.sleep(INTERVAL)
    request_model4 = RequestModel(source_url=CrawURL.AiQiYi_Series_SouthKorea_URL,
                                  platform=Platform.AiQiYi,
                                  video_category=VideoCategory.Series,
                                  series_region=SeriesRegion.SouthKorea)
    spider.start_craw(request_model=request_model4)
    time.sleep(INTERVAL)
    request_model5 = RequestModel(source_url=CrawURL.AiQiYi_Series_America_URL,
                                  platform=Platform.AiQiYi,
                                  video_category=VideoCategory.Series,
                                  series_region=SeriesRegion.America)
    spider.start_craw(request_model=request_model5)


# 抓取爱奇艺电影
def craw_aiqiyi_movie(spider):
    request_model1 = RequestModel(source_url=CrawURL.AiQiYi_Movie_All_URL,
                                  platform=Platform.AiQiYi,
                                  video_category=VideoCategory.Movie,
                                  movie_region= MovieRegion.All)
    spider.start_craw(request_model=request_model1)
    time.sleep(INTERVAL)
    request_model2 = RequestModel(source_url=CrawURL.AiQiYi_Movie_Chines_URL,
                                  platform=Platform.AiQiYi,
                                  video_category=VideoCategory.Movie,
                                  movie_region=MovieRegion.Chines)
    spider.start_craw(request_model=request_model2)
    time.sleep(INTERVAL)
    request_model3 = RequestModel(source_url=CrawURL.AiQiYi_Movie_Cinemas_URL,
                                  platform=Platform.AiQiYi,
                                  video_category=VideoCategory.Movie,
                                  movie_region=MovieRegion.Cinemas)
    spider.start_craw(request_model=request_model3)
    time.sleep(INTERVAL)
    request_model4 = RequestModel(source_url=CrawURL.AiQiYi_Movie_America_URL,
                                  platform=Platform.AiQiYi,
                                  video_category=VideoCategory.Movie,
                                  movie_region=MovieRegion.America)
    spider.start_craw(request_model=request_model4)


# 抓取爱奇艺综艺
def craw_aiqiyi_variety(spider):
    request_model1 = RequestModel(source_url=CrawURL.AiQiYi_Variety_All_URL,
                                  platform=Platform.AiQiYi,
                                  video_category=VideoCategory.Variety,
                                  veriety_region= VarietyType.All)
    spider.start_craw(request_model=request_model1)


# 抓取优酷视频电视剧
def craw_youku_series(spider):
    request_model1 = RequestModel(source_url=CrawURL.YouKu_Series_All_URL,
                                  platform=Platform.YouKuVido,
                                  video_category=VideoCategory.Series,
                                  series_region=SeriesRegion.All)
    spider.start_craw(request_model=request_model1)
    time.sleep(INTERVAL)
    request_model2 = RequestModel(source_url=CrawURL.YouKu_Series_Local_URL,
                                  platform=Platform.YouKuVido,
                                  video_category=VideoCategory.Series,
                                  series_region=SeriesRegion.Local)
    spider.start_craw(request_model=request_model2)
    time.sleep(INTERVAL)
    request_model3 = RequestModel(source_url=CrawURL.YouKu_Series_Net_URL,
                                  platform=Platform.YouKuVido,
                                  video_category=VideoCategory.Series,
                                  series_region=SeriesRegion.Net)
    spider.start_craw(request_model=request_model3)
    time.sleep(INTERVAL)
    request_model4 = RequestModel(source_url=CrawURL.YouKu_Series_SouthKorea_URL,
                                  platform=Platform.YouKuVido,
                                  video_category=VideoCategory.Series,
                                  series_region=SeriesRegion.SouthKorea)
    spider.start_craw(request_model=request_model4)
    time.sleep(INTERVAL)
    request_model5 = RequestModel(source_url=CrawURL.YouKu_Series_America_URL,
                                  platform=Platform.YouKuVido,
                                  video_category=VideoCategory.Series,
                                  series_region=SeriesRegion.America)
    spider.start_craw(request_model=request_model5)


# 抓取优酷视频电影
def craw_youku_movie(spider):
    request_model1 = RequestModel(source_url=CrawURL.YouKu_Movie_All_URL,
                                  platform=Platform.YouKuVido,
                                  video_category=VideoCategory.Movie,
                                  movie_region= MovieRegion.All)
    spider.start_craw(request_model=request_model1)
    time.sleep(INTERVAL)
    request_model2 = RequestModel(source_url=CrawURL.YouKu_Movie_Local_URL,
                                  platform=Platform.YouKuVido,
                                  video_category=VideoCategory.Movie,
                                  movie_region=MovieRegion.Local)
    spider.start_craw(request_model=request_model2)
    time.sleep(INTERVAL)
    request_model4 = RequestModel(source_url=CrawURL.YouKu_Movie_HongKong_URL,
                                  platform=Platform.YouKuVido,
                                  video_category=VideoCategory.Movie,
                                  movie_region=MovieRegion.HongKong)
    spider.start_craw(request_model=request_model4)
    time.sleep(INTERVAL)
    request_model5 = RequestModel(source_url=CrawURL.YouKu_Movie_America_URL,
                                  platform=Platform.YouKuVido,
                                  video_category=VideoCategory.Movie,
                                  movie_region=MovieRegion.America)
    spider.start_craw(request_model=request_model5)

# 抓取优酷综艺
def craw_youku_variety(spider):
    request_model1 = RequestModel(source_url=CrawURL.YouKu_Variety_All_URL,
                                  platform=Platform.YouKuVido,
                                  video_category=VideoCategory.Variety,
                                  veriety_region=VarietyType.All)
    spider.start_craw(request_model=request_model1)


def setup_logging(default_path="logging.yaml", default_level=logging.INFO, env_key="LOG_CFG"):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r") as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

if __name__ == '__main__':
    setup_logging(default_path="logging.yaml")

    spider = SpiderMain()
    # 腾讯
    craw_tx_series(spider)
    time.sleep(INTERVAL)
    craw_tx_movie(spider)
    time.sleep(INTERVAL)
    craw_tx_variety(spider)

    # 爱奇艺
    craw_aiqiyi_series(spider)
    time.sleep(INTERVAL)
    craw_aiqiyi_movie(spider)
    time.sleep(INTERVAL)
    craw_aiqiyi_variety(spider)

    # 优酷
    craw_youku_series(spider)
    time.sleep(INTERVAL)
    craw_youku_movie(spider)
    time.sleep(INTERVAL)
    craw_youku_variety(spider)
