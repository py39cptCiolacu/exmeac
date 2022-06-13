from flask import Blueprint, render_template, flash, redirect, request, session, url_for
from .models import Votes, Motion, Time
import time
from . import db


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():

    return render_template("home.html")

@views.route('/voting', methods=['GET', 'POST'])
def voting():

     t = time.localtime()
     now = time.strftime("%H:%M:%S", t)
     now = str(now)

     motion = Motion.query.order_by(Motion.id.desc()).first()

     if request.method == 'POST':
          vote_value = request.form.get('button')
          password =  session['parola']
          check = Votes.query.filter_by(password = password).first()
          if check:
               flash("You already voted!", category='error')
               return redirect(url_for('views.home'))
          elif status() == 'STOP':
               flash('No time to vote', category='error')
               return redirect(url_for('views.home'))
          else:     
               vote = Votes(vote = vote_value, password = password, time = now)
               db.session.add(vote)
               db.session.commit()
               flash('Congrats!', category='succes')
               return redirect(url_for('views.results_loading'))


     return render_template("voting.html", motion = motion)

def time_is_ok():
     pass

@views.route('/schedule', methods=['GET', 'POST'])
def scedule():

     return render_template("schedule.html")

@views.route('/results_loading', methods=['GET', 'POST'])
def results_loading():


     return render_template('results_loading.html')

@views.route('/results', methods=['GET', 'POST'])
def results():

     if status() == 'START':
          return redirect(url_for('views.results_loading')) 

     yes = 0
     no = 0
     abstention = 0 

     votes = Votes.query.all()
     for v in votes:
          if v.vote == 'yes':
               yes += 1
          if v.vote == 'no':
               no += 1
          if v.vote == 'abstention':
               abstention += 1

     if yes > (no + abstention):
          motion_status = "The motion is accepted!"
     if yes <= (no + abstention):
          motion_status = "The motion is declined!"

     return render_template("results.html", yes = yes, no = no, abstention = abstention, motion_status = motion_status)


def status():

     status = Time.query.order_by(Time.id.desc()).first()

     return status.time
