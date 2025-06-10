import os

class Config:
    SECRET_KEY = "zhihu_hot_data_visualization_secret_key"
    
    # MySQL数据库配置
    DB_USERNAME = os.environ.get("DB_USERNAME", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "123456")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_NAME = os.environ.get("DB_NAME", "zhihu_hot")
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False 