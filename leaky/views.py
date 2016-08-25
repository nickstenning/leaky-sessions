# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from pyramid.view import view_config


@view_config(route_name='debug', renderer='string')
def debug(request):
    import zope.sqlalchemy.datamanager
    return repr(zope.sqlalchemy.datamanager._SESSION_STATE)


@view_config(route_name='leaky', renderer='string')
def leaky(request):
    request.db.execute('SELECT 1')
    return 'This just leaked'


@view_config(route_name='notleaky', renderer='string')
def notleaky(request):
    request.db.execute('SELECT 1')
    return 'This was fine'


def includeme(config):
    config.scan(__name__)
    config.add_route('debug', '/')
    config.add_route('leaky', '/leaky')
    config.add_route('notleaky', '/notleaky')
