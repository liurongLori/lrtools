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
            if k == '${typically}' and '${typically' in answer:
                vs = random.choice(cv)
                cv.remove(vs)
                answer = answer.replace("${typically}", vs)
                vs = random.choice(cv)
                answer = answer.replace("${typically1}", vs)
            elif k == '${go on through}' and '${go on through' in answer:
                vs = random.choice(cv)
                cv.remove(vs)
                answer = answer.replace("${go on through}", vs)
                vs = random.choice(cv)
                answer = answer.replace("${go on through1}", vs)
            elif k == '${the best}' and '${the best' in answer:
                vs = random.choice(cv)
                cv.remove(vs)
                answer = answer.replace("${the best}", vs)
                vs = random.choice(cv)
                cv.remove(vs)
                answer = answer.replace("${the best 1}", vs)
                vs = random.choice(cv)
                cv.remove(vs)
                answer = answer.replace("${the best 2}", vs)
            elif k == '${products }' and '${products ' in answer:
                for i in range(3):
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
    random.seed(url)
    return [(qi, query_source[qi]) for qi in random.sample(list(query_source.keys()), 2)]
