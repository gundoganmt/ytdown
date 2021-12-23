from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from ytdown.models import Admin, Video, Faq
from datetime import datetime, timedelta
from ytdown import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
import calendar, random
from sqlalchemy import func

account = Blueprint('account',__name__)

@login_manager.user_loader
def load_user(id):
    return Admin.query.get(int(id))

@account.route('/dashboard')
def dashboard():
    two_months = (datetime.today()-timedelta(60)).strftime('%Y-%m-%d')
    one_month = (datetime.today()-timedelta(30)).strftime('%Y-%m-%d')

    two_weeks = (datetime.today()-timedelta(14)).strftime('%Y-%m-%d')
    one_week = (datetime.today()-timedelta(7)).strftime('%Y-%m-%d')

    yesterday = (datetime.today()-timedelta(1)).strftime('%Y-%m-%d')
    today = datetime.today().strftime('%Y-%m-%d')

    total_two_months = db.session.query(Video).filter(Video.dw_date > two_months).count()
    total_new_vid = db.session.query(Video).filter(Video.dw_date > one_month)

    total_two_weeks = db.session.query(Video).filter(Video.dw_date > two_weeks).count()
    week_new_vid = db.session.query(Video).filter(Video.dw_date > one_week)

    total_yesterday = db.session.query(Video).filter(Video.dw_date==yesterday).count()
    total_today = db.session.query(Video).filter(Video.dw_date==today).count()

    last_month = total_two_months - total_new_vid.count()
    last_week = total_two_weeks - week_new_vid.count()

    if not last_month==0:
        rate_month = 100*(total_new_vid.count()-last_month)/last_month
    else:
        rate_month=0.0
    if not last_week==0:
        rate_week = 100*(week_new_vid.count()-last_week)/last_week
    else:
        rate_week=0.0
    if not total_yesterday==0:
        rate_today = 100*(total_today-total_yesterday)/total_yesterday
    else:
        rate_today=0.0

    data = []
    vid = db.session.query(Video).first()

    if vid:
        start_date = datetime.strptime(vid.dw_date, '%Y-%m-%d')
        f_dw = vid.dw_date
    else:
        start_date = datetime.today()
        f_dw = start_date.strftime('%Y-%m-%d')

    month_later = start_date + timedelta(days=3)

    a = db.session.query(Video.dw_date, func.count(Video.dw_date)).group_by(Video.dw_date).order_by(Video.dw_date).all()

    delta = timedelta(days=1)
    i = 0
    while start_date <= month_later:
        try:
            if a[i][0] == start_date.strftime('%Y-%m-%d'):
                data.append(a[i][1])
                i += 1
            else:
                data.append(0)
        except:
            data.append(0)
        start_date += delta

        if datetime.today() > month_later:
            month_later += delta

    context = {
        "data": data,
        "f_dw": f_dw,
        "week_new_vid": week_new_vid.count(),
        "total_new_vid": total_new_vid.count(),
        "rate_week": rate_week,
        "rate_month": rate_month,
        'total_today': total_today,
        'rate_today': rate_today
    }

    return render_template('admin/dashboard.html', **context)

@account.route('/latest_downloads')
def latest_downloads():
    down_vids = Video.query.all()
    return render_template('admin/latest_downloads.html', down_vids=down_vids)

@account.route('/delete')
def delete():
    down_vids = Video.query.all()
    for i in down_vids:
        db.session.delete(i)
    db.session.commit()
    return "success"

@account.route('/p')
def p():
    start_date = datetime.today() - timedelta(days=10)
    today = datetime.today()

    while start_date <= today:
        for i in range(random.randint(0,10)):
            v = Video(web_url="https://www.g.com", dw_date=start_date.strftime('%Y-%m-%d'))
            db.session.add(v)
        start_date += timedelta(days=1)
    db.session.commit()
    return "success"

@account.route('/faq', methods=['GET', 'POST'])
def faq():
    if request.method == 'POST':
        faq_q = request.form['faq_q']
        faq_ans = request.form['faq_ans']

        new_faq = Faq(faq_q=faq_q, faq_ans=faq_ans)
        db.session.add(new_faq)
        db.session.commit()

        return redirect(request.url)

    else:
        all_faq = Faq.query.all()
        return render_template('admin/faq.html', all_faq=all_faq)


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

@account.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))
