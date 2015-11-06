#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import utf8
import re

from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.api import memcache
from google.appengine.ext.webapp.util import run_wsgi_app

import tenjin
from tenjin.helpers import escape, to_str
from tenjin.helpers.html import text2html
tengine = tenjin.Engine(layout="template/base.html", cache=tenjin.MemoryCacheStorage())

import mylist
import sil
import svl

def error_page(org, error_message):
    org.error(500)
    context = {
        'page_title': 'エラー',
        'error_message' : error_message,
    }
    org.response.out.write(tengine.render('template/error.html', context))

#
# トップページ
#
class IndexHandler(webapp.RequestHandler):
    def get(self):
        context = {
            'page_title' : 'ちょっとしたツール置き場',
        }
        self.response.out.write(tengine.render('template/index.html', context))

#
# マイリスト変換
#
class MylistHandler(webapp.RequestHandler):
    def get(self):
        context = {
            'page_title' : 'マイリストを貼り付け用iframeに変換',
        }
        self.response.out.write(tengine.render('template/mylist.html', context))

class MylistConvertHandler(webapp.RequestHandler):
    def post(self):
        url = self.request.get('url')
        r = re.compile("http://www\.nicovideo\.jp/(?:my/)?mylist/(?:#/)?(.*)")
        m = r.match(url)
        if not m:
            error_page(self, '正しいURLではありません。URLが間違っていないかを確認して下さい。')
        else:
            mylist_id = m.group(1)
            rss_url = 'http://www.nicovideo.jp/mylist/' + mylist_id + '?rss=2.0'
            
            response = urlfetch.fetch(rss_url)
            if not(response and response.status_code == 200):
                error_page(self, 'ダウンロードに失敗しました。マイリストが公開状態かを確認して下さい。')
            else:
                context = {
                    'page_title' : 'マイリスト変換結果',
                    'result' : mylist.convert(response.content),
                }
                self.response.out.write(tengine.render('template/mylist_convert.html', context))

#
# SIL問題変換
#
class SILHandler(webapp.RequestHandler):
    def get(self):
        context = {
            'page_title' : '『学辞郎』からP-Study System用SIL問題集を作成',
        }
        self.response.out.write(tengine.render('template/sil.html', context))

class SILConvertHandler(webapp.RequestHandler):
    def post(self):
        result = sil.convert(self.request.get('file'),
                             self.request.get('name'),
                             self.request.get('explanation'))
        
        self.response.headers["Content-Type"] = "text/plain"
        self.response.headers["Content-Disposition"] = "attachment; filename=\"%s.csv\"" % self.request.get('filename')
        self.response.out.write(result)        

#
# SVL問題変換
#
class SVLHandler(webapp.RequestHandler):
    def get(self):
        context = {
            'page_title' : '『英辞郎』からP-Study System用SVL問題集を作成',
        }
        self.response.out.write(tengine.render('template/svl.html', context))

class SVLConvertHandler(webapp.RequestHandler):
    def post(self):
        result = svl.convert(self.request.get('file'),
                             self.request.get('name'),
                             self.request.get('explanation'))
        
        self.response.headers["Content-Type"] = "text/plain"
        self.response.headers["Content-Disposition"] = "attachment; filename=\"%s.csv\"" % self.request.get('filename')
        self.response.out.write(result)        


def main():
    application = webapp.WSGIApplication([('/', IndexHandler),
                                          ('/mylist', MylistHandler),
                                          ('/mylist_convert', MylistConvertHandler),
                                          ('/sil', SILHandler),
                                          ('/sil_convert', SILConvertHandler),
                                          ('/svl', SVLHandler),
                                          ('/svl_convert', SVLConvertHandler),
                                         ],
                                         debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
