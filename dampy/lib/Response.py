# ashokkumar.ta@gmail.com / 24-May-2019

class Response:
    '''
    A response representation of an API call. It has
    success -> True (or) False indicating success or failure
    message -> An error message in case of failure
    data -> The response data
    '''

    def __init__(self, success, message, data):
        '''
         Initialize Response object   
        '''
        self.success = success
        self.message = message
        self.data = data

    def jsonify(self):
        '''
        Convert the response data to json
        '''
        self.data = self.data.json()
