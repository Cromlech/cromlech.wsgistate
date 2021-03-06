# -*- coding: utf-8 -*-

try:
    import cPickle as pickle
except ImportError:
    import pickle

import time
from wsgistate.file import FileCache
from wsgistate.session import SessionManager, CookieSession


class TimeoutException(Exception):

    def __init__(self, reason, default):
        Exception.__init__(self, reason)
        self.default = default


class TimeoutFileCache(FileCache):

    def get(self, key, default=None):
        try:
            exp, value = pickle.load(open(self._key_to_file(key), 'rb'))
            # Remove item if time has expired.
            if exp < time.time():
                self.delete(key)
                raise TimeoutException('Timeout', value)
            return value
        except (IOError, OSError, EOFError, pickle.PickleError):
            pass
        return default


class Manager(SessionManager):

    def _get(self, environ):
        try:
            return SessionManager._get(self, environ)
        except TimeoutException as timeout:
            self._sid, self.session = self._cache.create()
            self.new = True
            self.expired = True
            environ['session.timeout'] = timeout
    

class TimeoutCookieSession(CookieSession):

    def __call__(self, environ, start_response):
        # New session manager instance each time
        sess = Manager(self.cache, environ, **self.kw)
        environ[self.key] = sess
        try:
            # Return initial response if new or session id is random
            if sess.new:
                return self._initial(environ, start_response)
            return self.application(environ, start_response)
        # Always close session
        finally:
            sess.close()
