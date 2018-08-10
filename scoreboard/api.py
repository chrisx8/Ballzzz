import re
from flask_restful import Resource, reqparse
from models import Scoreboard
from views import DBSession, get_rankings
from sqlalchemy.orm.exc import NoResultFound

# Username legality check: 4-50 alphanumeric characters
USERNAME_REGEX = re.compile('^[a-zA-Z0-9._-]{4,50}$')

# accept and parse POST
score_parser = reqparse.RequestParser()
score_parser.add_argument('username',
                          help='Your username should contain 4-50 '
                          'characters, with only letters and numbers.',
                          required=True)
score_parser.add_argument('score',
                          help='This field is required', required=True)


# Score API
class PublishScore(Resource):
    # GET: get the top 5
    def get(self):
        top_ten = dict()
        # find all users, sorted by score
        board = DBSession.query(Scoreboard).order_by("score desc").all()
        # find top five users if there's more than 5 users
        if len(board) > 10:
            for i in range(10):
                # result contains username, score, ranking (handles ties)
                top_ten[i] = self.build_user_data_json(board, i)
        # otherwise find all users
        else:
            for i in range(len(board)):
                # result contains username, score, ranking (handles ties)
                top_ten[i] = self.build_user_data_json(board, i)
        # close DB session
        DBSession.close()
        return top_ten, 200

    # POST: submit score
    def post(self):
        data = score_parser.parse_args()
        # Find if user already exists
        try:
            user_data = DBSession.query(Scoreboard).\
                filter_by(username=data['username']).one()
            # If the user's score in database is lower, update score
            if user_data.score < int(data['score']):
                user_data.score = data.score
        # If user doesn't exist, create user and save score
        except NoResultFound:
            user_data = Scoreboard(username=data['username'],
                                   score=int(data['score']))
            DBSession.add(user_data)
        # Commit change to DB
        DBSession.commit()
        # Find current ranking
        board = DBSession.query(Scoreboard).order_by("score desc").all()
        # find index of user
        index = board.index(user_data)
        # close DB session
        DBSession.close()
        return self.build_user_data_json(board, index), 201
    
    def build_user_data_json(self, board, i):
        return {'username': board[i].username, 
                'score': board[i].score, 
                'ranking': get_rankings(board)[i]
                }
