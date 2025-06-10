from app import db
from datetime import datetime

class SentimentAnalysis(db.Model):
    __tablename__ = 'sentiment_analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('hot_articles.id'))
    sentiment_score = db.Column(db.Float)  # 情感分数，0-1，越接近1越积极
    positive_count = db.Column(db.Integer, default=0)  # 积极词汇数量
    negative_count = db.Column(db.Integer, default=0)  # 消极词汇数量
    neutral_count = db.Column(db.Integer, default=0)  # 中性词汇数量
    keywords = db.Column(db.Text)  # 关键词，以逗号分隔
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    article = db.relationship('HotArticle', backref=db.backref('sentiment', lazy=True))
    
    def __init__(self, article_id, sentiment_score, positive_count=0, negative_count=0, neutral_count=0, keywords=''):
        self.article_id = article_id
        self.sentiment_score = sentiment_score
        self.positive_count = positive_count
        self.negative_count = negative_count
        self.neutral_count = neutral_count
        self.keywords = keywords
    
    def to_dict(self):
        return {
            'id': self.id,
            'article_id': self.article_id,
            'sentiment_score': self.sentiment_score,
            'positive_count': self.positive_count,
            'negative_count': self.negative_count,
            'neutral_count': self.neutral_count,
            'keywords': self.keywords.split(',') if self.keywords else [],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f'<SentimentAnalysis {self.id} - Score: {self.sentiment_score}>' 