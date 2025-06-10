from flask import Blueprint, jsonify, request, session
from flask_cors import cross_origin
from app.models import User, HotArticle, SentimentAnalysis
from app.services.crawler_service import CrawlerService
from app.utils.text_analysis import perform_sentiment_analysis
from app import db
from collections import Counter
import jieba
import re
from datetime import datetime

mobile_api_bp = Blueprint('mobile_api', __name__, url_prefix='/api/mobile')

# 跨域支持
@mobile_api_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@mobile_api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'success',
        'message': '服务正常运行',
        'timestamp': datetime.now().isoformat()
    })

@mobile_api_bp.route('/auth/login', methods=['POST'])
def mobile_login():
    """移动端登录接口"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'status': 'error',
                'message': '用户名和密码不能为空'
            }), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.verify_password(password):
            # 生成简单的token（实际项目中应使用JWT）
            token = f"user_{user.id}_{datetime.now().timestamp()}"
            
            return jsonify({
                'status': 'success',
                'message': '登录成功',
                'data': {
                    'user_id': user.id,
                    'username': user.username,
                    'is_admin': user.is_admin,
                    'avatar_url': user.avatar_url,
                    'token': token
                }
            })
        else:
            return jsonify({
                'status': 'error',
                'message': '用户名或密码不正确'
            }), 401
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'登录失败: {str(e)}'
        }), 500

@mobile_api_bp.route('/auth/register', methods=['POST'])
def mobile_register():
    """移动端注册接口"""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({
                'status': 'error',
                'message': '所有字段都是必填的'
            }), 400
        
        # 检查用户是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({
                'status': 'error',
                'message': '用户名已存在'
            }), 400
            
        if User.query.filter_by(email=email).first():
            return jsonify({
                'status': 'error',
                'message': '邮箱已被注册'
            }), 400
        
        # 创建新用户
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '注册成功',
            'data': {
                'user_id': user.id,
                'username': user.username
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'注册失败: {str(e)}'
        }), 500

@mobile_api_bp.route('/hot_articles', methods=['GET'])
def get_mobile_hot_articles():
    """获取热门文章列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # 分页查询
        articles = HotArticle.query.order_by(HotArticle.rank).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'status': 'success',
            'data': {
                'articles': [article.to_dict() for article in articles.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': articles.total,
                    'pages': articles.pages,
                    'has_next': articles.has_next,
                    'has_prev': articles.has_prev
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取文章失败: {str(e)}'
        }), 500

@mobile_api_bp.route('/hot_articles/refresh', methods=['POST'])
def refresh_mobile_hot_articles():
    """刷新热门文章数据"""
    try:
        result = CrawlerService.refresh_hot_data()
        
        if result["status"] == "success":
            return jsonify({
                'status': 'success',
                'message': '数据刷新成功',
                'data': {
                    'count': len(result["data"]),
                    'articles': [article.to_dict() for article in result["data"][:10]]  # 只返回前10条
                }
            })
        else:
            return jsonify({
                'status': 'error',
                'message': result["message"]
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'刷新失败: {str(e)}'
        }), 500

@mobile_api_bp.route('/analysis/hot_words', methods=['GET'])
def get_mobile_hot_words():
    """获取热词分析数据"""
    try:
        limit = request.args.get('limit', 30, type=int)
        
        articles = HotArticle.query.all()
        
        # 提取所有文章标题和描述的文本
        all_text = ''
        for article in articles:
            all_text += article.title + ' ' + (article.description or '')
        
        # 中文分词
        words = jieba.cut(all_text)
        
        # 过滤停用词
        stop_words = {'的', '了', '和', '是', '在', '有', '被', '？', '如何', '为什么', '吗', '为何', '多', '大', '小', '上', '下', '年', '月', '日', '等', '中', '个', '这', '那', '什么', '哪些', '怎么', '还', '都', '就', '你', '我', '他', '她'}
        filtered_words = [word for word in words if len(word) > 1 and word not in stop_words]
        
        # 统计词频
        word_count = Counter(filtered_words).most_common(limit)
        
        return jsonify({
            'status': 'success',
            'data': {
                'hot_words': [{'word': word, 'count': count} for word, count in word_count],
                'total_words': len(filtered_words),
                'unique_words': len(set(filtered_words))
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取热词失败: {str(e)}'
        }), 500

@mobile_api_bp.route('/analysis/sentiment', methods=['GET'])
def get_mobile_sentiment():
    """获取情感分析数据"""
    try:
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
        
        # 计算总体情感统计
        total_positive = sum(s.positive_count for s in sentiment_analyses)
        total_negative = sum(s.negative_count for s in sentiment_analyses)
        total_neutral = sum(s.neutral_count for s in sentiment_analyses)
        avg_sentiment = sum(s.sentiment_score for s in sentiment_analyses) / len(sentiment_analyses) if sentiment_analyses else 0
        
        return jsonify({
            'status': 'success',
            'data': {
                'summary': {
                    'total_positive': total_positive,
                    'total_negative': total_negative,
                    'total_neutral': total_neutral,
                    'average_sentiment': round(avg_sentiment, 3)
                },
                'details': [
                    {
                        'article_id': s.article_id,
                        'sentiment_score': s.sentiment_score,
                        'positive_count': s.positive_count,
                        'negative_count': s.negative_count,
                        'neutral_count': s.neutral_count,
                        'keywords': s.keywords.split(',') if s.keywords else []
                    } for s in sentiment_analyses
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取情感分析失败: {str(e)}'
        }), 500

@mobile_api_bp.route('/analysis/stats', methods=['GET'])
def get_mobile_stats():
    """获取统计数据概览"""
    try:
        articles = HotArticle.query.all()
        
        # 基础统计
        total_articles = len(articles)
        total_hot_value = sum(int(re.sub(r'[^\d]', '', article.hot_value)) if re.sub(r'[^\d]', '', article.hot_value) else 0 for article in articles)
        total_answers = sum(article.answer_count for article in articles)
        
        # 排名分组统计
        rank_groups = {
            'top_10': len([a for a in articles if a.rank <= 10]),
            'top_20': len([a for a in articles if 11 <= a.rank <= 20]),
            'top_30': len([a for a in articles if 21 <= a.rank <= 30]),
            'others': len([a for a in articles if a.rank > 30])
        }
        
        return jsonify({
            'status': 'success',
            'data': {
                'overview': {
                    'total_articles': total_articles,
                    'total_hot_value': total_hot_value,
                    'total_answers': total_answers,
                    'last_updated': articles[0].created_at.isoformat() if articles else None
                },
                'rank_distribution': rank_groups
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取统计数据失败: {str(e)}'
        }), 500
