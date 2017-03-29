from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Video
import logging


class DataHandler(object):
    def __init__(self):
        engine = create_engine('mysql+pymysql://root:123456@localhost:3306/videoSpider?charset=utf8mb4')
        db_session = sessionmaker(bind=engine)
        self.session = db_session()

    def save_data(self, datas):
        if datas is None:
            return None
        for data in datas:
            if data.get('name') is None:
                return None
            if data.get('link') is None:
                return None

            new_video = Video(name=data.get('name'), image=data.get('image'), desc=data.get('desc'),
                              play_num=data.get('play_num'), update_num=data.get('update_num'), link=data.get('link'),
                              score=data.get('score'), video_category=data.get('video_category'), series_region=data.get('series_region'),
                              movie_region=data.get('movie_region'), veriety_region=data.get('veriety_region'), platform=data.get('platform'))
            try:
                self.session.add(new_video)
                self.session.commit()
            except Exception:
                self.session.rollback()
                logging.ERROR('database save failed.')
                raise Exception

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


