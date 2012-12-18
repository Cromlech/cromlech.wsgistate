# -*- coding: utf-8 -*-

from transaction import manager as transaction_manager
from wsgistate.simple import session as session_decorator
from .controlled import WsgistateSession


def session_wrapper(app, session_key, **gc):
    wrapper = session_decorator(key=session_key)
    return wrapper(app)


def session_application(app, session_key, session=False, **gc):
    """A simple app middleware that can use a generic transaction
    manager.
    """

    def sessionned_application(environ, start_response):
        if session is not False:
            tm = transaction_manager
        else:
            tm = None

        with WsgistateSession(environ, session_key, tm):
            return app(environ, start_response)

    wrapper = session_decorator(key=session_key)
    return wrapper(sessionned_application)
