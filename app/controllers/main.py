from flask import Blueprint, render_template, jsonify, redirect, url_for, flash
from app.models.hot_article import HotArticle
from app.services.crawler_service import CrawlerService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """主页"""
    # 从数据库获取最新数据
    result = CrawlerService.get_latest_data()
    if result["status"] == "success":
        articles = result["data"]
    else:
        articles = []
        flash(result["message"], "error")
    
    return render_template('index.html', articles=articles)

@main_bp.route('/refresh_data')
def refresh_data():
    """刷新知乎热榜数据"""
    result = CrawlerService.refresh_hot_data()
    if result["status"] == "success":
        flash("数据刷新成功！", "success")
    else:
        flash(result["message"], "error")
    return redirect(url_for('main.index'))

@main_bp.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')

@main_bp.route('/api/hot_articles')
def get_hot_articles():
    """API接口：获取热门文章"""
    articles = HotArticle.query.order_by(HotArticle.rank).all()
    return jsonify({
        'status': 'success',
        'data': [article.to_dict() for article in articles]
    })

@main_bp.route('/analysis/api/hot_articles')
def get_analysis_hot_articles():
    """API接口：获取热门文章（兼容路径）"""
    return get_hot_articles()

@main_bp.route('/api/refresh_hot_articles', methods=['POST'])
def refresh_hot_articles():
    """API接口：刷新热门文章数据"""
    result = CrawlerService.refresh_hot_data()
    if result["status"] == "success":
        return jsonify({
            'status': 'success',
            'message': '数据刷新成功',
            'data': [article.to_dict() for article in result["data"]]
        })
    else:
        return jsonify({
            'status': 'error',
            'message': result["message"]
        }), 500

@main_bp.route('/analysis/api/refresh_hot_articles', methods=['POST'])
def analysis_refresh_hot_articles():
    """API接口：刷新热门文章数据（兼容路径）"""
    return refresh_hot_articles() 