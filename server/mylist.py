#!/usr/local/bin/python
#-*- coding: utf-8 -*-

import re
from xml.etree.ElementTree import *

def convert(src):
    r = re.compile("http://www\.nicovideo\.jp/watch/(.*)")
    rst = ''
    
    root = XML(src) 
    channel = root.find('channel')
    for item in channel.findall('item'):
        #print """<a href="%s" target="_blank">%s</a>""" % (item.findtext('link'), item.findtext('title'))
        
        title = item.findtext('title')
        url = item.findtext('link')
        m = r.match(url)
        idnum = m.group(1)
        rst += """<iframe width="312" height="176" src="http://ext.nicovideo.jp/thumb/%s" scrolling="no" style="border:solid 1px #CCC;" frameborder="0"><a href="http://www.nicovideo.jp/watch/%s">%s</a></iframe>
""" % (idnum, idnum, title)
    return rst
