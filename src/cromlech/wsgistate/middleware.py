# -*- coding: utf-8 -*-

from wsgistate import session as session_decorator


def session_wrapper_factory(global_conf, session_key):
    wrapper = session_decorator(key=session_key)

    def session_app(app):
        return wrapper(app)

    return session_app
