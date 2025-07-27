from flask import render_template, url_for, redirect, session, flash, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from company_blog import db
from company_blog.models import User
from company_blog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from flask Blueprint

users = Blueprint('users',__name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                next = request.args.get('next')
                if next == None or not next[0] == '/':
                    next = url_for('users.user_maintenance')
                return redirect(next)
            else:
                flash('パスワードが一致しません')
        else:
            flash('入力されたユーザーは存在しません')

    return render_template('users/login.html', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/register', methods=['GET','POST'])
@login_required
def register():
    form = RegistrationForm()
    if not current_user.is_administrator():
        abort(403)
    if form.validate_on_submit():
        # session['email'] = form.email.data
        # session['username'] = form.username.data
        # session['password'] = form.password.data
        user = User(email=form.email.data, username=form.username.data, password=form.password.data, administrator="0")
        db.session.add(user)
        db.session.commit()
        flash('ユーザーが登録されました')
        return redirect(url_for('users.user_maintenance'))
    return render_template('users/register.html', form=form)

@users.route('/user_maintenance')
@login_required
def user_maintenance():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id).paginate(page=page, per_page=10)
    return render_template('users/user_maintenance.html', users=users)

@users.route('/<int:user_id>/account', methods=['GET', 'POST'])
@login_required
def account(user_id):
    user = User.query.get_or_404(user_id)
    if user.id != current_user.id and not current_user.is_administrator():
        abort(403)
    form = UpdateUserForm(user_id)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.password.data:
            user.password = form.password.data
        db.session.commit()
        flash('ユーザーアカウントが更新されました')
        return redirect(url_for('users.user_maintenance'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    return render_template('users/account.html', form=form)

@users.route('/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    user =User.query.get_or_404(user_id)
    if not current_user.is_administrator():
        abort(403)
    if user.is_administrator():
        flash('管理者は削除できません')
        return redirect(url_for('users.account', user_id=user_id))
    db.session.delete(user)
    db.session.commit()
    flash('ユーザーアカウントが削除されました')
    return redirect(url_for('users.user_maintenance'))