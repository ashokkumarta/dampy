
class Response:
    def __init__(self, success, message, data):
        self.success = success
        self.message = message
        self.data = data

    def jsonify(self):
        self.data = self.data.json()
