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
    return list(query_source.items())
