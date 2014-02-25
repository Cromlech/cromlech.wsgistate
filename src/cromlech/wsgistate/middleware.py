# -*- coding: utf-8 -*-

from transaction import manager as transaction_manager
from wsgistate.simple import session as session_decorator
from .controlled import WsgistateSession


def session_wrapper(app, *global_conf, **local_conf):
    session_key = local_conf.get('session_key', 'session')
    wrapper = session_decorator(key=session_key)
    return wrapper(app)
