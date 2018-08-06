from common import get_rankings
from models import DBSession, Scoreboard
from flask import render_template, Blueprint, flash, redirect

views = Blueprint('views', __name__, template_folder='templates')

# Homepage
@views.route('/')
def home():
    return render_template('index.html')

# Scoreboard page
@views.route('/scoreboard/')
def scoreboard():
    board = DBSession.query(Scoreboard).order_by("score desc").all()
    rankings = get_rankings(board)
    return render_template('scoreboard.html', scoreboard=board,
                           count=len(board), rankings=rankings)
