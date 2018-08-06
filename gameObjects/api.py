import requests

class API(object):
    def __init__(self, username, url="https://ballzzz.herokuapp.com"):
        self.username = username
        self.url = url + "/api/score/"

    # return data: result message (success or error)
    def uploadScore(self, score):
        # construct data to send to API
        postData = {'username': self.username, 'score': score}
        # send score to API
        try:
            postResponse = requests.post(self.url, postData)
        except:
            return {'message': 'Cannot connect to server'}
        # process API response status
        if postResponse.status_code == 201:
            ranking = postResponse.json()['ranking']
            return {'message': 'Score uploaded', 'ranking': ranking}
            # get and store ranking
        else:
            return {'message': postResponse.json()['message']}
