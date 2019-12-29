# Distributed Rate Limiter Service

from flask import Flask
from flask_jsonrpc import JSONRPC
from redis import Redis
from retrying import retry
import threading

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api')
redis = Redis(host='redis', port=6379)

RATE_LIMIT = 500
RATE_TIME = 60


class RedisWrite(threading.Thread):
    def __init__(self, user_id):
        threading.Thread.__init__(self)
        self.user_id = user_id

    def run(self):
        pipe = redis.pipeline()
        pipe.incr(self.user_id)
        pipe.expire(self.user_id, RATE_TIME)
        pipe.execute()
        return True


@jsonrpc.method('App.handle_request')
def handle_request(user_id):
    ok = check_rate(user_id)
    if not ok:
        return False
    # Write to redis asynchronously and return immediately
    RedisWrite(user_id).start()
    return True


@retry(stop_max_attempt_number=3)
def check_rate(user_id):
    # The rate may still be unset
    rate = redis.get(user_id) or 0
    # Check if the user reached his rate limit including this request
    if int(rate) >= RATE_LIMIT:
        return False
    else:
        return True


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

