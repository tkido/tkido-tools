#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import re
import webapp2

from google.appengine.api import memcache
from google.appengine.api import namespace_manager
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import ndb

import mylist
import sil
import svl
import tengine

def error_page(org, error_message):
    org.error(500)
    context = {
        'page_title': 'エラー',
        'error_message' : error_message,
    }
    org.response.out.write(tengine.render(':error', context))

#
# トップページ
#
class IndexHandler(webapp2.RequestHandler):
    def get(self):
        context = {
            'page_title' : 'ちょっとしたツール置き場',
        }
        self.response.out.write(tengine.render(':index', context))

#
# マイリスト変換
#
class MylistHandler(webapp2.RequestHandler):
    def get(self):
        context = {
            'page_title' : 'マイリストを貼り付け用iframeに変換',
        }
        self.response.out.write(tengine.render(':mylist', context))

class MylistConvertHandler(webapp2.RequestHandler):
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
                self.response.out.write(tengine.render(':mylist_convert', context))

#
# SIL問題変換
#
class SILHandler(webapp2.RequestHandler):
    def get(self):
        context = {
            'page_title' : '『学辞郎』からP-Study System用SIL問題集を作成',
        }
        self.response.out.write(tengine.render(':sil', context))

class SILConvertHandler(webapp2.RequestHandler):
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
class SVLHandler(webapp2.RequestHandler):
    def get(self):
        context = {
            'page_title' : '『英辞郎』からP-Study System用SVL問題集を作成',
        }
        self.response.out.write(tengine.render(':svl', context))

class SVLConvertHandler(webapp2.RequestHandler):
    def post(self):
        result = svl.convert(self.request.get('file'),
                             self.request.get('name'),
                             self.request.get('explanation'))
        
        self.response.headers["Content-Type"] = "text/plain"
        self.response.headers["Content-Disposition"] = "attachment; filename=\"%s.csv\"" % self.request.get('filename')
        self.response.out.write(result)        



app = webapp2.WSGIApplication([('/', IndexHandler),
                               ('/mylist', MylistHandler),
                               ('/mylist_convert', MylistConvertHandler),
                               ('/sil', SILHandler),
                               ('/sil_convert', SILConvertHandler),
                               ('/svl', SVLHandler),
                               ('/svl_convert', SVLConvertHandler),
                              ],
                              debug=True)
