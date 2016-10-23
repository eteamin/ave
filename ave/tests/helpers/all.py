from tg import config
from pyDes import triple_des


def make_auth_header():
    secret_key = config.get('auth_secret_key')
    auth_message = config.get('auth_message')
    return {'token': triple_des(secret_key).encrypt(auth_message, padmode=2)}


def keep_keys(keys, _dict):
    kept = {}

    def add(k):
        kept[k] = _dict[k]
    [add(k) for k in _dict.keys() if k in keys]
    return kept


# Test keep_keys
if __name__ == '__main__':
    a = {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': 4
    }
    assert keep_keys(['a', 'c'], a) == {'a': 1, 'c': 3}
