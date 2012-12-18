# -*- coding: utf-8 -*-

from .controlled import WsgistateSession
from wsgistate.simple import session as session_decorator


def session_wrapper(app, session_key, **gc):
    wrapper = session_decorator(key=session_key)
    return wrapper(app)
