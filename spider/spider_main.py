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
    America = '美国'

# 电影地区分类
@unique
class Movie_region(Enum):
    All = '热播'
    Cinemas = '院线'
    Chines = '华语'
    Local = '内地'
    HongKong = '港片'
    America = '美国'

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

        print('crawing:  %s:%s:%s:%s:%s' % (requestModel.source_url, requestModel.platform, requestModel.video_category, requestModel.source_url, requestModel.source_url.value))
        # return
        html_cont = self.downloader.download(requestModel.source_url.value)
        if html_cont is None:
            print('download fail.')
            return
        print('download success.')

        kw = {}
        if requestModel.series_region is not None:
            kw['series_region'] = requestModel.series_region.value
        if requestModel.movie_region is not None:
            kw['movie_region'] = requestModel.movie_region.value
        if requestModel.veriety_region is not None:
            kw['veriety_region'] = requestModel.veriety_region.value

        if requestModel.platform == Platform.TengXunVideo:
            try:
                crawed_datas = self.parser.parse_tx_video_data(requestModel.source_url, html_cont,
                                                               platform=requestModel.platform.value,
                                                               video_category=requestModel.video_category.value,
                                                               **kw
                                                               )
                if crawed_datas is None or len(crawed_datas) == 0:
                    print('not tx datas.')
                    return

                print('craw success!')
                self.data_handler.save_data(crawed_datas)
                # self.outputer.collect_data(crawed_datas)
            except Exception:
                print('craw tengxun video failed.')
                raise Exception

        elif requestModel.platform == Platform.AiQiYi:
            try:
                crawed_datas = self.parser.parse_aiqiyi_video_data(requestModel.source_url, html_cont,
                                                               platform=requestModel.platform.value,
                                                               video_category=requestModel.video_category.value,
                                                               **kw
                                                               )
                if crawed_datas is None or len(crawed_datas) == 0:
                    print('not aiqiyi datas.')
                    return
                print('craw success!')
                self.data_handler.save_data(crawed_datas)
                # self.outputer.collect_data(crawed_datas)
            except Exception:
                print('craw aiqiyi video failed.')
                raise Exception

        elif requestModel.platform == Platform.YouKuVido:
            try:
                crawed_datas = self.parser.parse_youku_video_data(requestModel.source_url, html_cont,
                                                               platform=requestModel.platform.value,
                                                               video_category=requestModel.video_category.value,
                                                               **kw
                                                               )
                if crawed_datas is None or len(crawed_datas) == 0:
                    print('not Youku datas.')
                    return
                print('craw success!')
                self.data_handler.save_data(crawed_datas)
                # self.outputer.collect_data(crawed_datas)
            except Exception:
                print('craw Youku video failed.')
                raise Exception
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
    requestModel5 = RequestModel(source_url=Craw_url.TX_Series_America_URL,
                                 platform=Platform.TengXunVideo,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.America)
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
    requestModel5 = RequestModel(source_url=Craw_url.TX_Movie_America_URL,
                                 platform=Platform.TengXunVideo,
                                 video_category=Video_category.Movie,
                                 movie_region=Movie_region.America)
    spider.start_craw(requestModel=requestModel5)

# 抓取腾讯综艺
def craw_tx_variety(spider):
    requestModel1 = RequestModel(source_url=Craw_url.TX_Variety_All_URL,
                                 platform=Platform.TengXunVideo,
                                 video_category=Video_category.Variety,
                                 veriety_region=Variety_type.All)
    spider.start_craw(requestModel=requestModel1)

# 爱奇艺电视剧
def craw_aiqiyi_series(spider):
    requestModel1 = RequestModel(source_url=Craw_url.AiQiYi_Series_All_URL,
                                 platform=Platform.AiQiYi,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.All)
    spider.start_craw(requestModel=requestModel1)
    time.sleep(INTERVAL)
    requestModel2 = RequestModel(source_url=Craw_url.AiQiYi_Series_Local_URL,
                                 platform=Platform.AiQiYi,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.Local)
    spider.start_craw(requestModel=requestModel2)
    time.sleep(INTERVAL)
    requestModel3 = RequestModel(source_url=Craw_url.AiQiYi_Series_Net_URL,
                                 platform=Platform.AiQiYi,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.Net)
    spider.start_craw(requestModel=requestModel3)
    time.sleep(INTERVAL)
    requestModel4 = RequestModel(source_url=Craw_url.AiQiYi_Series_SouthKorea_URL,
                                 platform=Platform.AiQiYi,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.SouthKorea)
    spider.start_craw(requestModel=requestModel4)
    time.sleep(INTERVAL)
    requestModel5 = RequestModel(source_url=Craw_url.AiQiYi_Series_America_URL,
                                 platform=Platform.AiQiYi,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.America)
    spider.start_craw(requestModel=requestModel5)

# 抓取爱奇艺电影
def craw_aiqiyi_movie(spider):
    requestModel1 = RequestModel(source_url=Craw_url.AiQiYi_Movie_All_URL,
                                 platform=Platform.AiQiYi,
                                 video_category=Video_category.Movie,
                                 movie_region= Movie_region.All)
    spider.start_craw(requestModel=requestModel1)
    time.sleep(INTERVAL)
    requestModel2 = RequestModel(source_url=Craw_url.AiQiYi_Movie_Chines_URL,
                                 platform=Platform.AiQiYi,
                                 video_category=Video_category.Movie,
                                 movie_region=Movie_region.Chines)
    spider.start_craw(requestModel=requestModel2)
    time.sleep(INTERVAL)
    requestModel3 = RequestModel(source_url=Craw_url.AiQiYi_Movie_Cinemas_URL,
                                 platform=Platform.AiQiYi,
                                 video_category=Video_category.Movie,
                                 movie_region=Movie_region.Cinemas)
    spider.start_craw(requestModel=requestModel3)
    time.sleep(INTERVAL)
    requestModel4 = RequestModel(source_url=Craw_url.AiQiYi_Movie_America_URL,
                                 platform=Platform.AiQiYi,
                                 video_category=Video_category.Movie,
                                 movie_region=Movie_region.America)
    spider.start_craw(requestModel=requestModel4)

# 抓取爱奇艺综艺
def craw_aiqiyi_variety(spider):
    requestModel1 = RequestModel(source_url=Craw_url.AiQiYi_Variety_All_URL,
                                 platform=Platform.AiQiYi,
                                 video_category=Video_category.Variety,
                                 veriety_region= Variety_type.All)
    spider.start_craw(requestModel=requestModel1)


# 抓取优酷视频电视剧
def craw_youku_series(spider):
    requestModel1 = RequestModel(source_url=Craw_url.YouKu_Series_All_URL,
                                 platform=Platform.YouKuVido,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.All)
    spider.start_craw(requestModel=requestModel1)
    time.sleep(INTERVAL)
    requestModel2 = RequestModel(source_url=Craw_url.YouKu_Series_Local_URL,
                                 platform=Platform.YouKuVido,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.Local)
    spider.start_craw(requestModel=requestModel2)
    time.sleep(INTERVAL)
    requestModel3 = RequestModel(source_url=Craw_url.YouKu_Series_Net_URL,
                                 platform=Platform.YouKuVido,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.Net)
    spider.start_craw(requestModel=requestModel3)
    time.sleep(INTERVAL)
    requestModel4 = RequestModel(source_url=Craw_url.YouKu_Series_SouthKorea_URL,
                                 platform=Platform.YouKuVido,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.SouthKorea)
    spider.start_craw(requestModel=requestModel4)
    time.sleep(INTERVAL)
    requestModel5 = RequestModel(source_url=Craw_url.YouKu_Series_America_URL,
                                 platform=Platform.YouKuVido,
                                 video_category=Video_category.Series,
                                 series_region=Series_region.America)
    spider.start_craw(requestModel=requestModel5)

# 抓取优酷视频电影
def craw_youku_movie(spider):
    requestModel1 = RequestModel(source_url=Craw_url.YouKu_Movie_All_URL,
                                 platform=Platform.YouKuVido,
                                 video_category=Video_category.Movie,
                                 movie_region= Movie_region.All)
    spider.start_craw(requestModel=requestModel1)
    time.sleep(INTERVAL)
    requestModel2 = RequestModel(source_url=Craw_url.YouKu_Movie_Local_URL,
                                 platform=Platform.YouKuVido,
                                 video_category=Video_category.Movie,
                                 movie_region=Movie_region.Local)
    spider.start_craw(requestModel=requestModel2)
    time.sleep(INTERVAL)
    requestModel4 = RequestModel(source_url=Craw_url.YouKu_Movie_HongKong_URL,
                                 platform=Platform.YouKuVido,
                                 video_category=Video_category.Movie,
                                 movie_region=Movie_region.HongKong)
    spider.start_craw(requestModel=requestModel4)
    time.sleep(INTERVAL)
    requestModel5 = RequestModel(source_url=Craw_url.YouKu_Movie_America_URL,
                                 platform=Platform.YouKuVido,
                                 video_category=Video_category.Movie,
                                 movie_region=Movie_region.America)
    spider.start_craw(requestModel=requestModel5)

# 抓取优酷综艺
def craw_youku_variety(spider):
    requestModel1 = RequestModel(source_url=Craw_url.YouKu_Variety_All_URL,
                                 platform=Platform.YouKuVido,
                                 video_category=Video_category.Variety,
                                 veriety_region=Variety_type.All)
    spider.start_craw(requestModel=requestModel1)

if __name__ == '__main__':
    spider = SpiderMain()
    腾讯
    craw_tx_series(spider)
    time.sleep(5)
    craw_tx_movie(spider)
    time.sleep(5)
    craw_tx_variety(spider)

    爱奇艺
    craw_aiqiyi_series(spider)
    time.sleep(5)
    craw_aiqiyi_movie(spider)
    time.sleep(5)
    craw_aiqiyi_variety(spider)

    优酷
    craw_youku_series(spider)
    time.sleep(5)
    craw_youku_movie(spider)
    time.sleep(5)
    craw_youku_variety(spider)
