from app import db
from datetime import datetime
import pytz


class HotArticle(db.Model):
    __tablename__ = 'hot_articles'

    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)  # 热榜排名
    title = db.Column(db.String(255))  # 热榜标题
    url = db.Column(db.String(255))  # 热榜链接
    hot_value = db.Column(db.String(64))  # 热度值
    answer_count = db.Column(db.Integer)  # 回答数
    description = db.Column(db.Text)  # 热榜描述
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')))

    def __init__(self, rank, title, url, hot_value, answer_count, description):
        self.rank = rank
        self.title = title
        self.url = url
        self.hot_value = hot_value
        self.answer_count = answer_count
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'rank': self.rank,
            'title': self.title,
            'url': self.url,
            'hot_value': self.hot_value,
            'answer_count': self.answer_count,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f'<HotArticle {self.title}>'


