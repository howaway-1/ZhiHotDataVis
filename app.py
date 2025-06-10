from app import create_app, db
from app.models import User, HotArticle, SentimentAnalysis
import os
import click
from app.utils.data_import import import_csv_data

app = create_app()

# 创建数据库表 - 替换了 before_first_request 装饰器
with app.app_context():
    db.create_all()

@app.cli.command('init-db')
def init_db_command():
    """清空并初始化数据库"""
    db.drop_all()
    db.create_all()
    click.echo('初始化数据库完成。')

@app.cli.command('create-admin')
@click.argument('username')
@click.argument('email')
@click.argument('password')
def create_admin(username, email, password):
    """创建管理员用户"""
    user = User(username=username, email=email, password=password, is_admin=True)
    db.session.add(user)
    db.session.commit()
    click.echo(f'管理员用户 {username} 创建成功！')

@app.cli.command('import-csv')
@click.argument('csv_path')
def import_csv(csv_path):
    """从CSV文件导入数据"""
    try:
        count = import_csv_data(csv_path)
        click.echo(f'成功导入 {count} 条数据。')
    except Exception as e:
        click.echo(f'导入失败: {str(e)}')

@app.shell_context_processor
def make_shell_context():
    """为Flask shell提供上下文"""
    return {
        'db': db,
        'User': User,
        'HotArticle': HotArticle,
        'SentimentAnalysis': SentimentAnalysis
    }

if __name__ == '__main__':
    # 确保instance文件夹存在
    if not os.path.exists('instance'):
        os.makedirs('instance')

    # 启动应用
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
