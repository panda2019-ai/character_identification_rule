# coding:utf-8
"""
"""

import codecs

question_flag_dict = dict()

with codecs.open('baike_qa_train_feature.txt', 'rb', 'utf-8', 'ignore') as infile:
    for line in infile:
        line = line.strip()
        if line:
            if line in question_flag_dict:
                question_flag_dict[line] += 1
            else:
                question_flag_dict[line] = 1

sorted_question_flag = sorted(question_flag_dict.items(), key=lambda x: x[1], reverse=True)

with open('question_flag.txt', 'wb') as outfile:
    for flag, cnt in sorted_question_flag:
        out_str = u'%s\t%d\n' % (flag, cnt)
        outfile.write(out_str.encode('utf-8', 'ignore'))
