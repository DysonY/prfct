def _add(x, y):
    for i in range(y):
        x += 1
    return x

def _pred(x):
    i = 0
    for j in range(x):
        i = j
    return i

def _sub(x, y):
    for i in range(y):
        x = _pred(x)
    return x

def _mul(x, y):
    i = 0
    for j in range(y):
        i = add(i, x)
    return i

def _nonzero(x):
    i = 0
    for j in range(x):
        i = 0
        i += 1
    return i

def _not(x):
    i = 0
    i += 1
    for j in range(x):
        i = 0
    return i

def _div(x, y):
    a = _not(_nonzero(y))
    n = 0
    for k in range(a):
        return n
    for i in range(x):
        b = _nonzero(_lt(x, y))
        for j in range(b):
            return n
        x = _sub(x, y)
        n += 1
    return n

def _copy(a, b):
    return b

def _copyadd(a, b):
    return _add(a, b)

def _copysub(a, b):
    return _sub(a, b)

def _copymul(a, b):
    return _mul(a, b)

def _copydiv(a, b):
    return _div(a, b)

def _and(x, y):
    c = 0
    a = _not(_nonzero(x))
    for i in range(a):
        return c
    b = _not(_nonzero(y))
    for j in range(b):
        return c
    d = 0
    d += 1
    return d

def _eq(x, y):
    g = _gte(x, y)
    l = _lte(x, y)
    c = _and(g, l)
    return c

def _lt(x, y):
    for i in range(x):
        y = pred(y)
    z = nonzero(y)
    return z

def _gt(x, y):
    c = _and(_not(_lt(x, y)), _not(_eq(x, y)))
    return c

def _lte(x, y):
    y += 1
    c = _lt(x, y)
    return c

def _gte(x, y):
    c = _not(_lt(x, y))
    return c

def _neq(x, y):
    c = _not(_eq(x, y))
    return c

