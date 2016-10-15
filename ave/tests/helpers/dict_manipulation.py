

def keep_keys(keys, _dict):
    kept = {}

    def add(k):
        kept[k] = _dict[k]
    [add(k) for k in _dict.keys() if k in keys]
    return kept
kept = {}


# Test
if __name__ == '__main__':
    a = {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': 4
    }
    assert keep_keys(['a', 'c'], a) == {'a': 1, 'c': 3}
