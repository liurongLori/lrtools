import copy
import os
import random
import sys

from .args_source import args_source_map


def replace_args(answer):
    count = 0
    while '${' in answer and count < 3:
        for k, v in args_source_map.items():
            cv = copy.deepcopy(v)
            if k == '${SUBREDDITS}' and '${SUBREDDITS' in answer:
                for i in range(3):
                    vs = random.choice(cv)
                    cv.remove(vs)
                    answer = answer.replace("${SUBREDDITS_%s}" % str(i + 1), vs)
            elif k == '${QUERY}' and '${QUERY' in answer:
                for i in range(2):
                    vs = random.choice(cv)
                    cv.remove(vs)
                    answer = answer.replace("${QUERY_%s}" % str(i + 1), vs)
            elif k == '${HOLIDAY_1}' and ('${HOLIDAY_1}' in answer or '${HOLIDAY_2}' in answer):
                for i in range(2):
                    vs = random.choice(cv)
                    cv.remove(vs)
                    answer = answer.replace("${HOLIDAY_%s}" % str(i + 1), vs)
            elif k == '${HOLIDAY_3}' and ('${HOLIDAY_3}' in answer or '${HOLIDAY_4}' in answer):
                for i in range(2):
                    vs = random.choice(cv)
                    cv.remove(vs)
                    answer = answer.replace("${HOLIDAY_%s}" % str(i + 3), vs)
            elif k in answer:
                if isinstance(v, list):
                    v = random.choice(v)
                answer = answer.replace(k, str(v))
        count += 1
    return answer


def rand_query(info):
    info = info.split('\t')
    query = info[2]
    q_index = info[5]
    if q_index == '8':
        flag = info[7]
        q_index += "_1"  if flag == "TRUE" else "_2"
    elif q_index == '9':
        flag = info[6]
        q_index += "_1"  if flag == "TRUE" else "_2"
    return [(q_index, query)]
