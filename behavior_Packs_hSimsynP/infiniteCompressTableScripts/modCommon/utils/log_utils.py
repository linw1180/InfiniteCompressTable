# -*- coding: utf-8 -*-

import functools
import logging
import sys

from .. import ModName


def func_log(func):
    @functools.wraps(func)
    def wrap_log(*args, **kwargs):
        logging.info("┌---------- Run %s --------------------┐" % func.__name__)
        if args:
            logging.info(args)
        if kwargs:
            logging.info(kwargs)

        result = func(*args, **kwargs)
        if result is not None:
            logging.info(" return:{}".format(result))
        logging.info("└---------- %s End --------------------┘" % func.__name__)
        return result

    return wrap_log


def make_common_logger():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(filename)s[%(lineno)d:] %(message)s')
    handler.setFormatter(formatter)
    lg = logging.getLogger(ModName)
    lg.handlers = []
    lg.addHandler(handler)
    lg.propagate = False
    return lg


logger = make_common_logger()
