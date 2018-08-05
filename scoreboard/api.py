import re
from flask_restful import Resource, reqparse
from models import Scoreboard
from views import DBSession, get_rankings
from sqlalchemy.orm.exc import NoResultFound

USERNAME_REGEX = re.compile('^[a-zA-Z0-9._-]{4,50}$')

score_parser = reqparse.RequestParser()
score_parser.add_argument('username',
                          help='Your username should contain with 4-50 '
                          'characters, with only letters and numbers.',
                          required=True)
score_parser.add_argument('score', help='This field is required', required=True)


class PublishScore(Resource):
    def post(self):
        data = score_parser.parse_args()
        update_score = False
        new_user = False
        try:
            find_user = DBSession.query(Scoreboard).\
                filter_by(username=data['username']).one()
            if find_user.score < int(data['score']):
                update_score = True
        except NoResultFound:
            new_user = True
        if new_user:
            new_score = Scoreboard(username=data['username'],
                                   score=int(data['score']))
            DBSession.add(new_score)
        elif update_score:
            new_score = DBSession.query(Scoreboard).\
                filter_by(username=data['username']).one()
            new_score.score = data.score
        else:
            new_score = DBSession.query(Scoreboard).\
                filter_by(username=data['username']).one()
        DBSession.commit()
        board = DBSession.query(Scoreboard).order_by("score desc").all()
        for i in range(len(board)):
            if board[i] == new_score:
                index = i
                break
        return {
            'username': new_score.username,
            'score': new_score.score,
            'ranking': get_rankings(board)[index]
        }, 201
