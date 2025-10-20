import copy
import os
import random
import sys

from .args_source import args_source_map
from .query_args import query_source


def replace_args(answer):
    count = 0
    while '${' in answer and count < 5:
        for k, v in args_source_map.items():
            cv = copy.deepcopy(v)
            if k == '${easter items}' and '${easter items' in answer:
                for i in range(5):
                    vs = random.choice(cv)
                    answer = answer.replace("${easter items%s}" % str(i+1), vs)
                    cv.remove(vs)
            elif k == '${Easter-themed products}' and '${festive essentials}' in answer:
                vs = random.choice(cv)
                answer = answer.replace("${Easter-themed products}", vs)
                cv.remove(vs)
                cv_1 = copy.deepcopy(args_source_map['${festive essentials}'])
                cv_1 += cv
                vs_1 = random.choice(cv_1)
                answer = answer.replace("${festive essentials}", vs_1)
            elif k in answer:
                if isinstance(v, list):
                    v = random.choice(v)
                answer = answer.replace(k, str(v))
        count += 1
    return answer


def rand_query(url):
    random.seed(url)
    q_1 = random.choice(['1', '2', '3', '4'])[0]
    if q_1 in ['2', '3']:
        q_2 = random.choice(['1', '4'])[0]
    else:
        q_2 = q_1
        while q_2 == q_1:
            q_2 = random.choice(['1', '2', '3', '4'])[0]
    # q_1 = '2'
    # q_2 = '2'
    return [(q_1, query_source[q_1]), (q_2, query_source[q_2])]
