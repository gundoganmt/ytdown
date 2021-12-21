from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from ytdown.models import Admin, Video
from datetime import datetime, date
from ytdown import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
import calendar, random
from sqlalchemy import func

account = Blueprint('account',__name__)

@login_manager.user_loader
def load_user(id):
    return Admin.query.get(int(id))

@account.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    data = []
    vid = db.session.query(Video).first()

    a = db.session.query(Video.download_date, func.count(Video.download_date)).group_by(Video.download_date).all()

    for i in a:
        print(type(i[0]), i[0])
    for i in range(31):
        if i%2 == 1:
            data.append(i*3)
        else:
            data.append(i*2)

    return render_template('admin/dashboard.html', data=data, f_dw=vid.download_date)

@account.route('/latest_downloads')
def latest_downloads():
    down_vids = Video.query.all()
    return render_template('admin/latest_downloads.html', down_vids=down_vids)

@account.route('/faq')
def faq():
    return render_template('admin/faq.html')


@account.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Admin.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('account.dashboard'))
            else:
                flash('Wrong Credentials! Check your spelling.')
                return render_template('account/login.html')
        else:
            flash('Wrong Credentials! Check your spelling.')
            return render_template('account/login.html')
    return render_template('account/login.html')

# @account.route('/signup', methods=['GET','POST'])
# def signup():
#     if current_user.is_authenticated:
#         return redirect(url_for('public.index'))
#     if request.method == 'POST':
#         name = request.form['name'].capitalize()
#         surname = request.form['surname'].capitalize()
#         email = request.form['email']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password, method='sha256')
#         existing_user = Users.query.filter_by(email=email).first()
#         if existing_user is None:
#             if email.startswith('demo'):
#                 user = Users(name=name, surname=surname, email=email,
#                     password=hashed_password, member_since=datetime.utcnow(),
#                     status='employer', email_approved=True)
#                 db.session.add(user)
#                 db.session.commit()
#             else:
#                 user = Users(name=name, surname=surname, email=email,
#                     password=hashed_password, member_since=datetime.utcnow(),
#                     status='employer')
#                 notif = Notification(notification_to=user, not_type=2)
#                 db.session.add(user)
#                 db.session.add(notif)
#                 db.session.commit()
#                 send_confirmation_email(user)
#             login_user(user)
#             return render_template('account/welcome.html')
#         flash('This email already being used!')
#         return render_template('account/signup.html')
#
#     return render_template('account/signup.html')

@account.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))
