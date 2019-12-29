# Distributed Rate Limiter Service

from flask import Flask
from flask_jsonrpc import JSONRPC
from redis import Redis
from retrying import retry

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api')
redis = Redis(host='redis', port=6379)

RATE_LIMIT = 500
RATE_TIME = 60


@jsonrpc.method('App.handle_request')
def handle_request(user_id):
    ok = check_rate(user_id)
    if not ok:
        return False
    pipe = redis.pipeline()
    pipe.incr(user_id)
    pipe.expire(user_id, RATE_TIME)
    pipe.execute()
    return True


@retry(stop_max_attempt_number=3)
def check_rate(user_id):
    # The rate may still be unset
    rate = redis.get(user_id) or 0
    if int(rate) >= RATE_LIMIT:
        return False
    else:
        return True


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

