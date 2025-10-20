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
            if k in answer:
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

    return [(q_1, query_source[q_1]), (q_2, query_source[q_2])]
