import pymysql
from app import create_app
from config import Config

def migrate_database():
    """
    为用户表添加头像字段
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
            # 检查avatar_url字段是否存在
            cursor.execute("SHOW COLUMNS FROM users LIKE 'avatar_url'")
            result = cursor.fetchone()
            
            if not result:
                # 添加avatar_url字段
                sql = "ALTER TABLE users ADD COLUMN avatar_url VARCHAR(255) DEFAULT NULL;"
                cursor.execute(sql)
                print("数据库迁移成功：users表添加了avatar_url字段")
            else:
                print("数据库迁移跳过：avatar_url字段已存在")
        
        # 提交更改
        connection.commit()
    
    except Exception as e:
        print(f"数据库迁移失败：{str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    migrate_database() 