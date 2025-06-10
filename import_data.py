from app import create_app, db
from app.utils.data_import import import_csv_data
import os
import sys

def main():
    csv_file = '知乎热榜.csv'
    if not os.path.exists(csv_file):
        print(f"错误：找不到文件 {csv_file}")
        return
    
    print(f"开始导入数据从 {csv_file}...")
    app = create_app()
    with app.app_context():
        try:
            # 确保数据库表存在
            db.create_all()
            # 导入数据
            count = import_csv_data(csv_file)
            print(f"成功导入 {count} 条数据")
        except Exception as e:
            print(f"导入失败: {str(e)}")

if __name__ == "__main__":
    main() 