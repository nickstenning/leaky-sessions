# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

import sqlalchemy
import transaction
import zope.sqlalchemy
from sqlalchemy.orm import sessionmaker

log = logging.getLogger(__name__)

Session = sessionmaker()


def _activate_hook(request):
    if request.path.startswith('/leaky'):
        return False
    return True


def _session(request):
    engine = request.registry['sqlalchemy.engine']
    session = Session(bind=engine)

    zope.sqlalchemy.register(session, transaction_manager=request.tm)

    @request.add_finished_callback
    def cleanup(r):
        # Try and find out under what conditions (i.e. for which requests) the
        # session is leaked.
        if id(session) in zope.sqlalchemy.datamanager._SESSION_STATE:
            log.warn('zope.sqlalchemy failed to clean up the session')
        session.close()

    return session


def includeme(config):
    config.add_settings({
        "tm.manager_hook": lambda request: transaction.TransactionManager(),
        "tm.activate_hook": _activate_hook,
        "tm.annotate_user": False,
    })
    config.include('pyramid_tm')

    engine = sqlalchemy.create_engine("postgresql://postgres@localhost/postgres")
    config.registry['sqlalchemy.engine'] = engine

    config.add_request_method(_session, name='db', reify=True)
