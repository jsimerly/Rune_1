import time

def time_it(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f'{func.__name__}: {t2-t1}')
        return result
    return wrapper