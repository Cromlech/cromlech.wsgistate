# -*- coding: utf-8 -*-
"""Wsgistate integration to the cromlech stack

The session is meant to be unique for the application. In the same way as zope
attach the site manager to current thread, session is attached to computing
thread by the application.

The session is automatically saved at end of context manager if no exceptions
occurs
"""

import crom
import UserDict
from cromlech.session.interfaces import ISession, ISaveableSessionTransactor
from transaction.interfaces import IDataManagerSavepoint
from wsgistate.session import SessionManager
from zope.interface import implements


class SessionStateException(Exception):
    pass


class State(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<SessionState %r>' % self.name


CLEAN = State('clean')
UNSAVED = State('modified')
ABORTED = State('aborted')
CLOSED = State('closed')


class Savepoint(UserDict.UserDict):
    implements(IDataManagerSavepoint)

    def __init__(self, transactor, data):
        UserDict.UserDict.__init__(self)
        self.transactor = transactor
        self.update(data)

    def rollback(self):
        self.transactor.data.clear()
        self.transactor.update(self.data)


class WsgistateSession(UserDict.UserDict):
    implements(ISession, ISaveableSessionTransactor)

    save = None
    state = CLEAN

    def __init__(self, manager):
        self.manager = manager
        self._last_commit = self.canonical = manager.session
        self.data = manager.session.copy()

    @property
    def session(self):
        return self

    def savepoint(self):
        if self.state is UNSAVED:
            self.save = Savepoint(self, self.data)
            self.state = CLEAN
        elif self.state in [ABORTED, CLOSED]:
            raise SessionStateException(
                "Session's current state disallows saving operations.")
        return self.save

    def __persist(self, data):
        self.manager.session = data

    def commit(self):
        self._last_commit = self.data.copy()
        self.__persist(self._last_commit)

    def __setitem__(self, name, value):
        if self.state not in [CLOSED, ABORTED]:
            self.state = UNSAVED
            UserDict.UserDict.__setitem__(self, name, value)
        else:
            raise KeyError(name, value)
            raise SessionStateException(
                "Session's current state disallows writing")

    def abort(self):
         if self.state not in [ABORTED, CLOSED]:
             self.clear()
             self.data = self._last_commit
             self.save = None
             self.state = ABORTED

    def finish(self):
        pass


@crom.adapter
@crom.sources(SessionManager)
@crom.target(ISession)
@crom.implements(ISession)
def wsgistate_session(manager):
    return manager.session


@crom.adapter
@crom.sources(SessionManager)
@crom.target(ISaveableSessionTransactor)
@crom.implements(ISession, ISaveableSessionTransactor)
def wsgistate_transactor(manager):
    return WsgistateSession(manager)
