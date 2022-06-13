from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from . import db
from .models import Motion, Time, Votes, Password
import pandas as pd

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():

    passwords = Password.query.all()
    passwords_text = []

    for p in passwords:
        passwords_text.append(p.password)

    if request.method == 'POST':
            parola = request.form.get('password_public')
            if parola == 'adminIB':
                return redirect(url_for('auth.admin_IB'))
            elif parola in passwords_text:
                session['parola'] = parola
                return redirect(url_for('views.voting'))
            else:
                flash('Incorrect password', category='error')

    return render_template("login.html")

@auth.route('/admin_IB', methods = ['GET', 'POST'])
def admin_IB():

    return render_template('admin_IB.html')


@auth.route('/admin_IB_time', methods = ['GET', 'POST'])
def admin_IB_time():

    if request.method == 'POST':
        time = request.form.get('time')
        time = Time(time = time)
        db.session.add(time)
        db.session.commit()

    return render_template('admin_IB_time.html')


@auth.route('/admin_IB_motion', methods = ['GET', 'POST'])
def admin_IB_motion():

    if request.method == 'POST':
        motion_text = request.form.get('motion')
        motion = Motion(motion = motion_text)
        db.session.add(motion)
        db.session.commit()
        flash("Motion set!")
        return redirect(url_for('views.voting'))        

    return render_template('admin_IB_motion.html')

@auth.route('/admin_IB_reset', methods = ['GET', 'POST'])
def admin_IB_reset():

    if request.method == 'POST':
        reset = request.form.get('reset')
        if reset == 'RESET-DATABASE':
            Votes.query.delete()
            motion = Motion(motion='No motion right now!')
            db.session.add(motion)
            db.session.commit()
            return redirect(url_for('views.voting'))


    return render_template('admin_IB_reset.html')

@auth.route('/admin_IB_password', methods = ['GET', 'POST'])
def admin_IB_password():

    if request.method == 'POST':
        Password.query.delete()   
        no_of_pass = request.form.get('nopass')
        if no_of_pass == 'GETPASSWORDS':
            passwords_text = get_passwords()
            for p in passwords_text:
                db.session.add(Password(password=p))
                db.session.commit()
            
    passwords = Password.query.all()

    return render_template('admin_IB_password.html', passwords = passwords)


def get_passwords():
     
    passwords = pd.read_excel('/home/cptdaniel/Documents/cpt/proiecte_python/P12-Voting-ExMEAC/website//codes.xls')
    passwords_text = []

    print(passwords)
    for p in passwords['Codes']:
        passwords_text.append(p)

    return passwords_text


