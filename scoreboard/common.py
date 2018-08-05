import secrets
import string


def create_session_key(length):
    key = ""
    characters = string.ascii_letters + string.digits + string.punctuation
    for i in range(length):
        key += secrets.choice(characters)
    print("Created a new session key")
    return key


def get_rankings(ordered_board):
    rankings = []
    rank = 1
    for i in range(len(ordered_board)):
        if i == 0:
            rankings.append(rank)
        elif ordered_board[i-1].score == ordered_board[i].score:
            rankings.append(rank)
        else:
            rank += 1
            rankings.append(rank)
    return rankings
