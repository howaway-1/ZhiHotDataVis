import pymysql
from app import create_app, db
from config import Config

def migrate_database():
    """
    修改用户表中password_hash字段的长度为255
    """
    try:
        # 创建数据库连接
        connection = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USERNAME,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        
        with connection.cursor() as cursor:
            # 修改users表中password_hash字段的长度为255
            sql = "ALTER TABLE users MODIFY COLUMN password_hash VARCHAR(255) NOT NULL;"
            cursor.execute(sql)
        
        # 提交更改
        connection.commit()
        print("数据库迁移成功：users表的password_hash字段长度已修改为255")
    
    except Exception as e:
        print(f"数据库迁移失败：{str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    migrate_database() 