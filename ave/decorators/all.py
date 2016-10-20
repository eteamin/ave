from tg import request, abort, config
from pyDes import triple_des


def is_authorized(f):
    def wrapper(*args, **kwargs):
        secret_key = config.get('auth_secret_key')
        auth_message = config.get('auth_message')
        if 'HTTP_TOKEN' not in request.environ:
            abort(401, detail='Authentication failed', passthrough='json')
        gibberish = request.environ['HTTP_TOKEN']
        if triple_des(secret_key).decrypt(gibberish, padmode=2).decode() != auth_message:
            abort(401, detail='Authentication failed', passthrough='json')
    return wrapper
