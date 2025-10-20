# coding=utf-8

import argparse
import os
import random
from datetime import datetime

# from halloween.answer_source_markdown import answer_source_map
# from halloween.generator import rand_query, replace_args
# from veterans.answer_source_markdown import answer_source_map
# from veterans.generator import rand_query, replace_args
# from military.answer_source_markdown import answer_source_map
# from military.generator import rand_query, replace_args
from normal.answer_source_markdown import answer_source_map
from normal.generator import rand_query, replace_args
# from thanksgiving.answer_source_markdown import answer_source_map
# from thanksgiving.generator import rand_query, replace_args
# from blackfriday.answer_source_markdown import answer_source_map
# from blackfriday.generator import rand_query, replace_args
# from cybermonday.answer_source_markdown import answer_source_map
# from cybermonday.generator import rand_query, replace_args
# from christmas.answer_source_markdown import answer_source_map
# from christmas.generator import rand_query, replace_args
# from newyear.answer_source_markdown import answer_source_map
# from newyear.generator import rand_query, replace_args
# from valentines.answer_source_markdown import answer_source_map
# from valentines.generator import rand_query, replace_args
# from easter.answer_source_markdown import answer_source_map
# from easter.generator import rand_query, replace_args
# from mothersday.answer_source_markdown import answer_source_map
# from mothersday.generator import rand_query, replace_args
# from memorialday.answer_source_markdown import answer_source_map
# from memorialday.generator import rand_query, replace_args

char_list = [',', '.', '!', '?', ':', '\n']


def format_answer(answer):
    # print(answer)
    answer = replace_args(answer)
    # print(answer)
    le = len(answer)
    i = 0
    t = ''
    while i < le:
        c = answer[i]
        if c != '$':
            if i == 0:
                c = c.upper()
            elif i - 2 >= 0 and answer[i - 2] in char_list and answer[i - 1] == ' ' and answer[i - 2] != ',':
                c = c.upper()
            elif i - 2 >= 0 and answer[i - 1] == '*' and answer[i - 2] == '*':
                c = c.upper()
            elif i - 3 >= 0 and answer[i - 3] == '*' and answer[i - 2] == '*' and answer[i - 1] == ' ':
                c = c.upper()
        t += c
        i += 1
    return t.replace('\n', '\\n')
    #.replace('- **', ' - **')


def gen_answer(qindex):
    answer_list = []
    for sentence in answer_source_map[qindex]:
        source = sentence.get('source')
        s = random.choice(source)
        if len(answer_list) == 0 or (answer_list[-1] in char_list and answer_list[-1] != ','):
            s = s[0].upper() + s[1:]
        if s[-1] in char_list:
            s += " "
        answer_list.append(s)
    return format_answer(''.join(answer_list))


def main(url):
    if "手写模板" not in url:
        return
    for qindex, query in rand_query(url):
        answer = gen_answer(qindex)
        yield f"{url}\t{answer}"
    # flag = True
    # if len(qindex.split('_')) == 2:
    #     qi, flag = qindex.split('_')
    #     yield f"{url}\t{qi}\t{query}\t{answer}\t{flag != '2'}"
    # else:
    #     yield f"{url}\t{qindex}\t{query}\t{answer}"
    #     # yield f"{url}\t{qindex}\t{query}\t{answer}\t{flag}"


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument('-d', '--directory', help="The project's directory", required=True)
    parse.add_argument('-f', '--file', help="The urls file", required=True)
    args = parse.parse_args()
    res_fn = os.path.join((os.getcwd()), args.directory, "qa_res_%s.tsv" % datetime.now().strftime("%Y-%m-%d"))
    print("start", datetime.now())
    with open(res_fn, 'w') as wf:
        with open(args.file) as f:
            for url in f.readlines():
                for qa in main(url.replace('\n', '')):
                    wf.write(qa)
                    wf.write('\n')
    print("end", datetime.now())
