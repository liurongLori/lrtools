import re


def _replace(answer, brand_name):
    if 'typically' not in answer.lower():
        return answer
    pattern = re.compile('typically', re.IGNORECASE)
    start, end = re.search(pattern, answer).span()
    assert answer[end] in [',', ' '], answer
    while answer[end] in [',', ' ']:
        end += 1
    if answer[start] == 'T' and not answer[end:].startswith(brand_name):
        return _replace(answer[:start] + answer[end].upper() + answer[end+1:], brand_name)
    return _replace(answer[:start] + answer[end:], brand_name)


if __name__ == '__main__':
    with open('chatgpt_answer.tsv') as f:
        for line in f.readlines():
            answer, brand_name = line.strip().split('\t')
            new_answer = _replace(answer, brand_name)
            print(answer, new_answer, sep='\t')