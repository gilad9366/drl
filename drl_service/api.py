# Distributed Rate Limiter Service

# Import framework
from flask import Flask
from flask_restful import Resource, Api

# Instantiate the app
app = Flask(__name__)
api = Api(app)


class RateLimit(Resource):
    USERS = {}

    def get(self, user_id):
        rate = self.USERS.get(user_id, 0)
        return "User " + user_id + " made " + str(rate) + " requests"

    def put(self, user_id):
        rate = self.USERS.get(user_id, 0)
        self.USERS[user_id] = rate + 1
        return "User " + user_id + " made a request"


# Create routes
api.add_resource(RateLimit, '/<string:user_id>')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

