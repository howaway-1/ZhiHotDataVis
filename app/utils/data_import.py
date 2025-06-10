import pandas as pd
import os
from app.models import HotArticle
from app import db

def import_csv_data(csv_file_path):
    """
    从CSV文件导入热榜数据到数据库
    
    Args:
        csv_file_path: CSV文件路径
    
    Returns:
        导入的记录数
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"文件不存在: {csv_file_path}")
        
        # 读取CSV文件
        df = pd.read_csv(csv_file_path, encoding='utf-8')
        
        # 清空现有数据
        HotArticle.query.delete()
        
        # 导入数据
        for _, row in df.iterrows():
            try:
                article = HotArticle(
                    rank=row['热榜排名'],
                    title=row['热榜标题'],
                    url=row['热榜链接'],
                    hot_value=row['热度值'],
                    answer_count=row['回答数'],
                    description=row['热榜描述']
                )
                db.session.add(article)
            except Exception as e:
                print(f"导入数据时出错: {e}, 行: {row}")
        
        # 提交事务
        db.session.commit()
        
        return len(df)
    
    except Exception as e:
        db.session.rollback()
        raise e 