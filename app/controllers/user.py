from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import os
import uuid
from app.models.user import User
from app import db

user_bp = Blueprint('user', __name__, url_prefix='/user')

# 允许的图片格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """检查文件是否是允许的格式"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    """用户个人资料页面"""
    # 检查用户是否登录
    if not session.get('user_id'):
        flash('请先登录', 'warning')
        return redirect(url_for('auth.login'))
    
    # 获取当前用户
    user = User.query.get(session.get('user_id'))
    if not user:
        flash('用户不存在', 'danger')
        return redirect(url_for('auth.logout'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        # 更新个人资料
        if action == 'update_profile':
            username = request.form.get('username')
            email = request.form.get('email')
            
            # 检查用户名唯一性
            if username != user.username and User.query.filter_by(username=username).first():
                flash('用户名已存在', 'danger')
                return redirect(url_for('user.profile'))
            
            # 检查邮箱唯一性
            if email != user.email and User.query.filter_by(email=email).first():
                flash('邮箱已被使用', 'danger')
                return redirect(url_for('user.profile'))
            
            # 更新用户资料
            user.username = username
            user.email = email
            db.session.commit()
            
            # 更新会话
            session['username'] = username
            
            flash('个人资料更新成功', 'success')
            return redirect(url_for('user.profile'))
        
        # 更新密码
        elif action == 'update_password':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            # 验证当前密码
            if not check_password_hash(user.password_hash, current_password):
                flash('当前密码不正确', 'danger')
                return redirect(url_for('user.profile'))
            
            # 验证新密码一致性
            if new_password != confirm_password:
                flash('两次输入的新密码不一致', 'danger')
                return redirect(url_for('user.profile'))
            
            # 更新密码
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            
            flash('密码更新成功', 'success')
            return redirect(url_for('user.profile'))
        
        # 上传头像
        elif action == 'upload_avatar':
            if 'avatar' not in request.files:
                flash('未选择文件', 'danger')
                return redirect(url_for('user.profile'))
            
            file = request.files['avatar']
            
            if file.filename == '':
                flash('未选择文件', 'danger')
                return redirect(url_for('user.profile'))
            
            if file and allowed_file(file.filename):
                # 创建上传目录（如果不存在）
                avatar_dir = os.path.join(current_app.static_folder, 'uploads', 'avatars')
                os.makedirs(avatar_dir, exist_ok=True)
                
                # 生成安全的文件名
                filename = secure_filename(file.filename)
                ext = filename.rsplit('.', 1)[1].lower()
                new_filename = f"{uuid.uuid4().hex}.{ext}"
                
                # 保存文件
                file_path = os.path.join(avatar_dir, new_filename)
                file.save(file_path)
                
                # 更新用户头像URL
                avatar_url = f"/static/uploads/avatars/{new_filename}"
                
                # 检查是否有旧头像需要删除
                if user.avatar_url and 'ui-avatars.com' not in user.avatar_url:
                    try:
                        old_avatar_path = os.path.join(current_app.root_path, 'static', user.avatar_url.lstrip('/static/'))
                        if os.path.exists(old_avatar_path):
                            os.remove(old_avatar_path)
                    except Exception as e:
                        print(f"删除旧头像出错: {str(e)}")
                
                # 更新数据库
                user.avatar_url = avatar_url
                db.session.commit()
                
                # 更新会话
                session['avatar_url'] = avatar_url
                
                flash('头像上传成功', 'success')
                return redirect(url_for('user.profile'))
            else:
                flash('不支持的文件格式', 'danger')
                return redirect(url_for('user.profile'))
    
    return render_template('user/profile.html', user=user) 