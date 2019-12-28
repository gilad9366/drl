# Distributed Rate Limiter Service

from flask import Flask
from flask_jsonrpc import JSONRPC
from redis import Redis
from retrying import retry

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api')
redis = Redis(host='redis', port=6379)


@jsonrpc.method('App.handle_request')
def handle_request(user_id):
    ok = check_rate()
    if not ok:
        return False
    pipe = redis.pipeline()
    pipe.incr(user_id)
    pipe.expire(user_id, 500)
    pipe.execute()
    return True


@retry(stop_max_attempt_number=3)
def check_rate(user_id):
    rate = redis.get(user_id)
    if rate >= 499:
        return False
    else:
        return True


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

