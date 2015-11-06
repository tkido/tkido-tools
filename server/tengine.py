#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import logging
import re

import tenjin
import tenjin.gae
from tenjin.helpers import escape, to_str
from tenjin.helpers.html import text2html

tenjin.gae.init()
logging.basicConfig(level=logging.DEBUG)
tenjin.logger = logging
tengine = tenjin.Engine(path=['template'], postfix='.html', layout=':base')

def render(tempalte, context, **kwargs):
    return tengine.render(tempalte, context, **kwargs)
