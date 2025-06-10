from flask import Blueprint, render_template, jsonify, request
from app.models import HotArticle, SentimentAnalysis
from app.utils.text_analysis import generate_word_cloud, perform_sentiment_analysis
from app import db
from collections import Counter
import jieba
import re

analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')

@analysis_bp.route('/dashboard')
def dashboard():
    """分析仪表盘页面"""
    return render_template('analysis/dashboard.html')

@analysis_bp.route('/hot_words')
def hot_words():
    """热词分析页面"""
    return render_template('analysis/hot_words.html')

@analysis_bp.route('/sentiment')
def sentiment():
    """情感分析页面"""
    return render_template('analysis/sentiment.html')

@analysis_bp.route('/article_stats')
def article_stats():
    """文章统计分析页面"""
    return render_template('analysis/article_stats.html')

@analysis_bp.route('/word_cloud')
def word_cloud():
    """词云图页面"""
    return render_template('analysis/word_cloud.html')

# API 接口
@analysis_bp.route('/api/hot_words_data')
def get_hot_words_data():
    """获取热词数据"""
    articles = HotArticle.query.all()
    
    # 提取所有文章标题和描述的文本
    all_text = ''
    for article in articles:
        all_text += article.title + ' ' + (article.description or '')
    
    # 中文分词
    words = jieba.cut(all_text)
    
    # 过滤停用词（简单过滤）
    stop_words = {'的', '了', '和', '是', '在', '有', '被', '？', '如何', '为什么', '吗', '为何', '多', '大', '小', '上', '下', '年', '月', '日', '等', '中', '个', '这', '那', '什么', '哪些', '怎么', '还', '都', '就', '你', '我', '他', '她'}
    filtered_words = [word for word in words if len(word) > 1 and word not in stop_words]
    
    # 统计词频
    word_count = Counter(filtered_words).most_common(30)
    
    return jsonify({
        'status': 'success',
        'data': [{'word': word, 'count': count} for word, count in word_count]
    })

@analysis_bp.route('/analysis/api/hot_words_data')
def get_analysis_hot_words_data():
    """获取热词数据（兼容路径）"""
    return get_hot_words_data()

@analysis_bp.route('/api/sentiment_data')
def get_sentiment_data():
    """获取情感分析数据"""
    sentiment_analyses = SentimentAnalysis.query.all()
    
    # 如果没有情感分析数据，则自动执行情感分析
    if not sentiment_analyses:
        articles = HotArticle.query.all()
        for article in articles:
            text = article.title + ' ' + (article.description or '')
            score, pos_count, neg_count, neu_count, keywords = perform_sentiment_analysis(text)
            
            # 创建情感分析记录
            sentiment = SentimentAnalysis(
                article_id=article.id,
                sentiment_score=score,
                positive_count=pos_count,
                negative_count=neg_count,
                neutral_count=neu_count,
                keywords=','.join(keywords)
            )
            db.session.add(sentiment)
        
        db.session.commit()
        sentiment_analyses = SentimentAnalysis.query.all()
    
    return jsonify({
        'status': 'success',
        'data': [sentiment.to_dict() for sentiment in sentiment_analyses]
    })

@analysis_bp.route('/analysis/api/sentiment_data')
def get_analysis_sentiment_data():
    """获取情感分析数据（兼容路径）"""
    return get_sentiment_data()

@analysis_bp.route('/api/article_stats_data')
def get_article_stats_data():
    """获取文章统计数据"""
    articles = HotArticle.query.all()
    
    # 计算统计数据
    hot_value_stats = [int(re.sub(r'[^\d]', '', article.hot_value)) if re.sub(r'[^\d]', '', article.hot_value) else 0 for article in articles]
    answer_count_stats = [article.answer_count for article in articles]
    
    # 计算按排名分组的热度值
    rank_groups = {
        '前10名': sum(hot_value_stats[:10]) if len(hot_value_stats) >= 10 else sum(hot_value_stats),
        '11-20名': sum(hot_value_stats[10:20]) if len(hot_value_stats) >= 20 else (sum(hot_value_stats[10:]) if len(hot_value_stats) > 10 else 0),
        '21-30名': sum(hot_value_stats[20:30]) if len(hot_value_stats) >= 30 else (sum(hot_value_stats[20:]) if len(hot_value_stats) > 20 else 0)
    }
    
    return jsonify({
        'status': 'success',
        'data': {
            'hot_value_stats': {
                'max': max(hot_value_stats) if hot_value_stats else 0,
                'min': min(hot_value_stats) if hot_value_stats else 0,
                'avg': sum(hot_value_stats) / len(hot_value_stats) if hot_value_stats else 0,
                'total': sum(hot_value_stats)
            },
            'answer_count_stats': {
                'max': max(answer_count_stats) if answer_count_stats else 0,
                'min': min(answer_count_stats) if answer_count_stats else 0,
                'avg': sum(answer_count_stats) / len(answer_count_stats) if answer_count_stats else 0,
                'total': sum(answer_count_stats)
            },
            'rank_groups': rank_groups,
            'articles': [article.to_dict() for article in articles]
        }
    })

@analysis_bp.route('/analysis/api/article_stats_data')
def get_analysis_article_stats_data():
    """获取文章统计数据（兼容路径）"""
    return get_article_stats_data()

@analysis_bp.route('/api/word_cloud_data')
def get_word_cloud_data():
    """获取词云图数据"""
    articles = HotArticle.query.all()
    
    # 提取所有文章标题和描述的文本
    all_text = ''
    for article in articles:
        all_text += article.title + ' ' + (article.description or '')
    
    # 生成词云图数据
    word_cloud_data = generate_word_cloud(all_text)
    
    return jsonify({
        'status': 'success',
        'data': word_cloud_data
    })

@analysis_bp.route('/analysis/api/word_cloud_data')
def get_analysis_word_cloud_data():
    """获取词云图数据（兼容路径）"""
    return get_word_cloud_data()

@analysis_bp.route('/api/refresh_sentiment_data', methods=['POST'])
def refresh_sentiment_data():
    """刷新情感分析数据"""
    try:
        # 清空现有的情感分析数据
        db.session.query(SentimentAnalysis).delete()
        db.session.commit()
        
        # 获取最新的热榜文章
        articles = HotArticle.query.all()
        
        # 为每篇文章执行情感分析
        for article in articles:
            text = article.title + ' ' + (article.description or '')
            score, pos_count, neg_count, neu_count, keywords = perform_sentiment_analysis(text)
            
            # 创建情感分析记录
            sentiment = SentimentAnalysis(
                article_id=article.id,
                sentiment_score=score,
                positive_count=pos_count,
                negative_count=neg_count,
                neutral_count=neu_count,
                keywords=','.join(keywords)
            )
            db.session.add(sentiment)
        
        db.session.commit()
        
        # 返回最新的情感分析数据
        sentiment_analyses = SentimentAnalysis.query.all()
        
        return jsonify({
            'status': 'success',
            'message': '情感分析数据已刷新',
            'data': [sentiment.to_dict() for sentiment in sentiment_analyses]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'刷新情感分析数据失败: {str(e)}'
        }), 500

@analysis_bp.route('/analysis/api/refresh_sentiment_data', methods=['POST'])
def analysis_refresh_sentiment_data():
    """刷新情感分析数据（兼容路径）"""
    return refresh_sentiment_data() 