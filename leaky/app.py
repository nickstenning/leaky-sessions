# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

from pyramid.config import Configurator

log = logging.getLogger(__name__)


def create_app(global_config, **settings):
    config = Configurator(settings=settings)
    config.include(__name__)
    return config.make_wsgi_app()


def includeme(config):
    config.include('.db')
    config.include('.views')
