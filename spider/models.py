from sqlalchemy import Column, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import time

BaseModel = declarative_base()


class Video(BaseModel):
    __tablename__ = 'video'

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    name = Column(String(80), nullable=False)
    image = Column(String(200))
    desc = Column(String(100))
    play_num = Column(String(50))
    update_num = Column(String(50))
    link = Column(String(200))
    score = Column(String(10))

    platform = Column(String(10), nullable=False)  # 来源平台
    video_category = Column(String(10), nullable=False)  # 视频大分类：电视剧、电影、综艺
    series_region = Column(String(20))  # 电视剧地区分类：全部热播、内地、网剧、韩剧、美剧
    movie_region = Column(String(20))  # 电影地区分类：全部热播、院线、内地、香港、美国
    veriety_region = Column(String(20))  # 综艺分类：热门

    created_at = Column(BigInteger, default=time.time)

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/videoSpider?charset=utf8mb4')
BaseModel.metadata.create_all(engine)
"""
data = {
                'name' : name.get_text(),
                'image' : 'http:' + image.get('r-lazyload'),
                'desc' : ' '.join(desc.get_text().strip().split()),
                'play_number' : num.get_text(),
                'update_status' : status,
                'link' : link.get('href')
            }

# 视频类型：电视剧、电影、综艺
Video_large_type = Enum('Video_large_type', ('Series', 'Movies', 'Variety'))
# 电视剧类型：全部热播、内地、网剧、韩剧、美剧
Series_region = Enum('Series_region', ('All', 'Local', 'Net', 'SouthKorea', 'EuropeAndAmerica'))
# 电影类型：全部热播、院线、内地、香港、美国
Movie_region = Enum('Movie_region', ('All', 'Cinemas', 'Local', 'HongKong', 'America'))
# 综艺类型：全部热播
Variety_type = Enum('Variety_type', ('Hot'))
"""

class RequestModel(object):
    def __init__(self, source_url, platform, video_category, *, series_region=None, movie_region=None, veriety_region=None):
        self.source_url = source_url
        self.platform = platform
        self.video_category = video_category
        self.series_region = series_region
        self.movie_region = movie_region
        self.veriety_region = veriety_region



