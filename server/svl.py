#!/usr/local/bin/python
#-*- coding: utf-8 -*-

import re

    
def convert(src, name, explanation):
    """
    """
    tmp = src.decode("utf-16")
    
    # 発音記号に含まれる改行を削除
    def delete_newline_in_phonetic_symbol(src):
        if len(src) < 20:
            return src
        else:
            return src + '\n'
    lines = tmp.split('\n')
    lines = map(delete_newline_in_phonetic_symbol, lines)
    tmp = ''.join(lines)
    
    lines = tmp.split('\n')
    
    def delete_phonetic_symbol(tmp):
        r = re.compile(u'\[.*?(?=[【])')
        tmp = r.sub('', tmp)
        r = re.compile(u'【[＠略同反対類複]】[^【 \\\\\n]*')
        tmp = r.sub('', tmp)
        r = re.compile(u'【(分節|参考|変化|語源|注意|無性語)】[^【\\\\\n]*')
        tmp = r.sub('', tmp)
        r = re.compile(u'【解説[^【\\\\\n]*')
        tmp = r.sub('', tmp)
        r = re.compile(u'【直後に[^【\\\\\n]*')
        tmp = r.sub('', tmp)
        r = re.compile(u'\\\\ ?・[^【\\\\\n]*')
        tmp = r.sub('', tmp)
        r = re.compile(u'◆[^【\\\\\n]*')
        tmp = r.sub('', tmp)
        r = re.compile(u'\s*(\\\\\s*)*$')
        tmp = r.sub('', tmp)
        
        r = re.compile(u'\s*///\s*')
        tmp = r.sub('\",\"', tmp)
        r = re.compile(u'\s*\\\\\s*')
        tmp = r.sub('\",\"', tmp)
        
        return '"' + tmp + '"'
        
    lines = map(delete_phonetic_symbol, lines)
    
    tmp = '\n'.join(lines)
    
    
    # ヘッダーを作成
    header = """psscsvfile,100,,,
%s,,,,
%s,,,,
a1,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,
""" % (name, explanation)
    
    # ヘッダーをつける
    tmp = header + tmp
    
    # Shift-JISに再変換
    rst = tmp.encode("cp932")
    return rst
