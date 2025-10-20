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
            if k == '${adv}' and '${adv' in answer:
                for i in range(2):
                    vs = random.choice(cv)
                    cv.remove(vs)
                    answer = answer.replace("${adv %s}" % str(i + 1), vs)
            elif k == '${material}' and '${material' in answer:
                for i in range(2):
                    vs = random.choice(cv)
                    cv.remove(vs)
                    answer = answer.replace("${material %s}" % str(i + 1), vs)
            elif k == '${products }' and '${products ' in answer:
                for i in range(4):
                    vs = random.choice(cv)
                    cv.remove(vs)
                    answer = answer.replace("${products %s}" % str(i + 1), vs)
            elif k in answer:
                if isinstance(v, list):
                    v = random.choice(v)
                answer = answer.replace(k, str(v))
        count += 1
    return answer


def rand_query(url):
    # random.seed(url)
    q_1 = random.choice(list(query_source.keys()))[0]
    q_index = q_1
    if q_1 in ['4', '6']:
        while q_index in ['4', '6', q_1]:
            q_index = random.choice(list(query_source.keys()))
        assert q_index not in ['4', '6']
    else:
        while q_index == q_1:
            q_index = random.choice(list(query_source.keys()))
    assert q_1 != q_index, "%s %s" % (q_1, q_index)
    return [(q_1, query_source[q_1]), (q_index, query_source[q_index])]
