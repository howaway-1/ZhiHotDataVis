from app.models.user import User
from app.models.hot_article import HotArticle
from app.models.sentiment_analysis import SentimentAnalysis

__all__ = ['User', 'HotArticle', 'SentimentAnalysis']


'''作用：定义 app.models 包的公共接口，统一导出模型类。
功能：
导入并导出 User, HotArticle, SentimentAnalysis 模型类。
允许其他模块通过 from app.models import User 访问模型，而无需直接导入子模块。
项目中的角色：
作为模型模块的入口，组织数据库模型（User 用于用户管理，HotArticle 存储热榜数据，SentimentAnalysis 存储情感分析结果）。
与 db（Flask-SQLAlchemy）配合，支持数据库操作。
'''