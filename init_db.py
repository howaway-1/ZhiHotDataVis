import pymysql
from app import create_app, db
from config import Config

def init_database():
    # 创建数据库连接
    connection = pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USERNAME,
        password=Config.DB_PASSWORD
    )
    
    try:
        with connection.cursor() as cursor:
            # 创建数据库
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {Config.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')
            print(f"数据库 {Config.DB_NAME} 创建成功！")
    finally:
        connection.close()
    
    # 创建应用上下文并初始化表结构
    app = create_app()
    with app.app_context():
        db.create_all()
        print("数据库表结构创建成功！")

if __name__ == '__main__':
    init_database()