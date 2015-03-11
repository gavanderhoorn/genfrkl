



def uniqify(iterable, key):
    seen = []
    for element in iterable:
        k = key(element)
        if k not in seen:
            seen.append(k)
            yield element
