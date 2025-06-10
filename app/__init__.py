from flask import Flask, session, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import os
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(Config)
    
    db.init_app(app)
    
    # 注册蓝图
    from app.controllers import register_blueprints
    register_blueprints(app)
    
    # 登录验证中间件
    @app.before_request
    def check_login():
        # 允许访问的路径，无需登录
        allowed_routes = [
            'main.index',  # 首页
            'auth.login',  # 登录页面
            'auth.register',  # 注册页面
            'static'  # 静态资源
        ]
        
        # 检查当前路径是否需要登录
        if not session.get('user_id'):
            # 如果不是允许的路径且未登录，则重定向到登录页面
            if request.endpoint and not any(route in request.endpoint for route in allowed_routes):
                flash('请先登录以访问该页面', 'warning')
                return redirect(url_for('auth.login'))
    
    return app 