# Distributed Rate Limiter Service

# Import framework
from flask import Flask
from flask_restful import Resource, Api
from redis import Redis

# Instantiate the app
app = Flask(__name__)
api = Api(app)
cache = Redis(host='redis', port=6379)


class RateLimit(Resource):

    def get(self, user_id):
        rate = cache.incr(user_id)
        return "User " + user_id + " made " + str(rate) + " requests"

    def put(self, user_id):
        cache.incr(user_id)
        return "User " + user_id + " made a request"


# Create routes
api.add_resource(RateLimit, '/<string:user_id>')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

