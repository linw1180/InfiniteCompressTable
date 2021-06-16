# -*- coding: utf-8 -*-

import functools
import time


def func_log(func):
    @functools.wraps(func)
    def wrap_log(*args, **kwargs):
        print "---------- Run %s --------------------" % func.__name__
        print "           ", time.strftime("%m-%d %H:%M:%S", time.localtime())
        if args:
            print args
        if kwargs:
            print kwargs
        result = func(*args, **kwargs)  # 此处拿到了被装饰的函数func
        if result is not None:
            print " return:", result
        print "---------- %s End --------------------" % func.__name__
        return result

    return wrap_log
