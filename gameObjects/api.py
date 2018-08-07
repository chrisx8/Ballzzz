import requests

class API(object):
    def __init__(self, username, url="https://ballzzz.herokuapp.com"):
        self.username = username
        self.url = url + "/api/score/"

    def uploadScore(self, score):
        # construct data to send to API
        postData = {'username': self.username, 'score': score}
        # send score to API
        try:
            postResponse = requests.post(self.url, postData)
        except:
            # return error message when connection fails
            return {'message': 'Cannot connect to server'}
        # API response is successful
        if postResponse.status_code == 201:
            # get and store ranking
            ranking = postResponse.json()['ranking']
            # return success message and raking
            return {'message': 'Score uploaded', 'ranking': ranking}
        else:
            # return error message from server
            return {'message': postResponse.json()['message']}
    
    def getTopFive(self):
        # get top five scores from API
        try:
            getResponse = requests.get(self.url)
        except:
            # return error message when connection fails
            return {'message': 'Cannot connect to server'}
        # API response is successful
        if getResponse.status_code == 200:
            # return success message and raking
            return {'message': 'Score uploaded', 'response': getResponse}
        else:
            # return error message from server
            return {'message': getResponse.json()['message']}
