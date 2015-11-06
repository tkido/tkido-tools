#!/usr/local/bin/python
#-*- coding: utf-8 -*-

import re

def convert(src, name, explanation):
    """
    """
    tmp = src.decode("cp932")
    # 行頭のダブルクォーテーションを消去。
    r = re.compile('^\"')
    tmp = r.sub('', tmp)
    
    # 半角カンマ+半角スペースを全角カンマに変換。
    r = re.compile(', ')
    tmp = r.sub('，', tmp)
    
    # 区切りを半角カンマに変換。
    r = re.compile(u'(?:：)|(?: \\\\ ・?)|(?: /// )')
    tmp = r.sub(',', tmp)
    
    # ヘッダーを作成
    header = """psscsvfile,100,,,
%s,,,,
%s,,,,
a1,q1,h1,h2
""" % (name, explanation)
    
    # ヘッダーをつける
    tmp = header + tmp
    
    # Shift-JISに再変換
    rst = tmp.encode("cp932")
    return rst
