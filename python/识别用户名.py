# coding:utf-8
"""
识别出《QQ群聊》语料中的“@用户名”这种mention
"""

import codecs
import re


# 识别mention
def identify_mention(utterance, regex_exp):
    mention_li = []
    # 去掉邮箱地址
    utterance = re.sub(u'[a-zA-Z0-9]+@[a-zA-Z0-9.]+', u'', utterance)
    # 去掉程序语言关键词
    utterance = re.sub(u'@array', u'', utterance)

    match_li = re.findall(regex_exp, utterance)
    if match_li:
        mention_li = match_li
    return mention_li


# 读入《QQ群聊》数据
utterance_li = []
with codecs.open('data/qqdata.txt', 'rb', 'utf-8', 'ignore') as infile:
    for line in infile:
        line = line.strip()
        if line:
            items_li = line.split(u'\t')
            if len(items_li) != 3:
                # print("数据格式有误：", line)
                continue
            else:
                user_id, user_name, utterance = items_li
                utterance_li.append((user_name, utterance))

print("len(utterance_li) = %d" % len(utterance_li))


# 输出提取出的mention
outfile_mention_context = open('mention_context.txt', 'wb')
outfile = open('mention_username.txt', 'wb')
for utterance_ser, (user_name, utterance) in enumerate(utterance_li):
    mention_li = identify_mention(utterance, u'@[^\s，。!]+')
    mention_str = u'##'.join(mention_li)
    out_str = u'%s\t%s\n' % (mention_str, utterance)
    outfile.write(out_str.encode('utf-8', 'ignore'))
    if mention_li:
        pre_utterance_li = utterance_li[utterance_ser-10:utterance_ser]
        pro_utterance_li = utterance_li[utterance_ser+1:utterance_ser+11]

        # print(len(pre_utterance_li))
        # print(pre_utterance_li)
        # print(len(pro_utterance_li))
        # print(pro_utterance_li)
        # print(utterance)
        # input()

        out_str = u'\n'.join([u'\t'.join(w) for w in pre_utterance_li])
        out_str += u'\n'
        out_str += u'\t'.join(("["+user_name+"]"+"["+mention_str+"]", utterance))
        out_str += u'\n'
        out_str += u'\n'.join([u'\t'.join(w) for w in pro_utterance_li])
        out_str += u'\n'
        out_str += u'#'*10
        out_str += u'\n\n'
        outfile_mention_context.write(out_str.encode('utf-8', 'ignore'))

outfile.close()
outfile_mention_context.close()

# 输出提取出的代词
outfile = open('mention_pronoun.txt', 'wb')
for user_name, utterance in utterance_li:
    mention_li = identify_mention(utterance, u'[你我他她]')
    mention_str = u'##'.join(mention_li)
    out_str = u'%s\t%s\n' % (mention_str, utterance)
    outfile.write(out_str.encode('utf-8', 'ignore'))
outfile.close()
