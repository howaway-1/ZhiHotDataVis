# Controllers package
from app.controllers.main import main_bp
from app.controllers.auth import auth_bp
from app.controllers.analysis import analysis_bp
from app.controllers.user import user_bp
from app.controllers.mobile_api import mobile_api_bp

def register_blueprints(app):
    """注册所有蓝图"""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(mobile_api_bp)