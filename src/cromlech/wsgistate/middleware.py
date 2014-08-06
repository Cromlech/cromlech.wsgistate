# -*- coding: utf-8 -*-

import tempfile
from transaction import manager as transaction_manager
from wsgistate.simple import session as session_decorator
from wsgistate.file import session as file_session_decorator
from .controlled import WsgistateSession


def session_wrapper(app, *global_conf, **local_conf):
    session_key = local_conf.pop('session_key', 'session')
    wrapper = session_decorator(key=session_key, **local_conf)
    return wrapper(app)


def file_session_wrapper(app, *global_conf, **local_conf):
    session_key = local_conf.pop('session_key', 'session')
    path = local_conf.get('session_cache', tempfile.gettempdir())
    wrapper = file_session_decorator(path, key=session_key, **local_conf)
    return wrapper(app)
