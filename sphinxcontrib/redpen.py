#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
"""
redpen extention

:copyright: Copyright 2016 by WAKAYAMA Shirou
:license: Apache Software License 2.0
"""

import httplib
import urllib
import os
import json
from functools import partial
import logging
from docutils.utils import relative_path


from docutils import nodes

from sphinx.ext.todo import todo_node

logger = logging.getLogger(__name__)
default_warn_logger = logger.warn


ftpl = "{file}: {lineno},{sp}-{ep}: {src}"
mtpl = "    {0}"


def post(host, port, text, lang, config):
    conn = httplib.HTTPConnection(host, port)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    b = {
        "format": "json2",
        "documentParser": "PLAIN",
        "config": config,
        "document": text.encode('utf-8'),
        "lang": lang,
    }
    body = urllib.urlencode(b)

    path = "/rest/document/validate"

    conn.request("POST", path, body=body, headers=headers)
    res = conn.getresponse()
    ret = res.read()
    conn.close()
    return ret

def validate(node, arg, warn=default_warn_logger):
    text = node.astext()
    if not text:
        return text

    r = post(arg["server"], arg["port"], text, arg["lang"], arg["config"])

    result(json.loads(r), arg, warn)

def result(ret, arg, warn=default_warn_logger):
    for e in ret['errors']:
        m = {
            "file": arg["docname"],
            "lineno": arg["lineno"],
            "sp": e['position']['start']['offset'],
            "ep": e['position']['end']['offset'],
            "src": e['sentence'].encode('utf-8'),
        }
        print(ftpl.format(**m))

        for error in e['errors']:
            msg = error['message'].encode('utf-8')
            print(mtpl.format(msg))
    
def get_file_path(app):
    return os.path.join(app.confdir, app.config.redpen_configfile)

def doctree_resolved(app, doctree, docname):
    filepath = get_file_path(app)
    config = open(filepath).read()
    lang = app.config.language
    if lang is None:
        lang = "ja"

    server = app.config.redpen_server
    port = app.config.redpen_port

    def text_not_in_literal(node):
        return (isinstance(node, nodes.Text) and
               not isinstance(node.parent,
                              (nodes.literal,
                               nodes.literal_block,
                               nodes.raw,
                               nodes.comment,
                              )) and
               not isinstance(node.parent.parent,
                              (todo_node,
                              ))
               )

    logger_method = getattr(app, app.config.redpen_loglevel.lower())
    def logger_func(term, lineno):
        location = '%s:%s' % (app.env.doc2path(docname), lineno or '')
        msg = u'%s: redpen:\n%s' % (location, term)
        logger_method(msg)

    for node in doctree.traverse(text_not_in_literal):
        lineno = node.line or node.parent.line or node.parent.parent.line
        arg = {
            "docname": docname,
            "lineno": lineno,
            "server": server,
            "port": port,
            "lang": lang,
            "config": config,
        }

        validate(node, arg, partial(logger_func, lineno=lineno))

def setup(app):
    app.add_config_value('redpen_server', True, 'env')
    app.add_config_value('redpen_port', True, 'env')
    app.add_config_value('redpen_loglevel', True, 'env')
    app.add_config_value('redpen_configfile', None, 'env')

    app.connect('doctree-resolved', doctree_resolved)


if __name__ == '__main__':
    config = open("test.conf.xml").read()

    r = post("localhost", 8080, "いわゆるRDBの設計で言うところのテーブル設計ですね。", "ja", config)
    print(r)
