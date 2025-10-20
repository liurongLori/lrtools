from datetime import datetime
import re

length = 6


def split_to_word(paragraph):
    pattern = r"[\w'\_\$\{\}\/]+"
    matches = re.findall(pattern, paragraph)
    c = 0
    res = []
    while c + length < len(matches) + length:
        i = c
        if c+length <= len(matches):
            s = ' '.join(matches[i:i+length])
            if '${' not in s:
                res.append(s)
            c = i + 1
        else:
            break
    return res


if __name__ == '__main__':
    print("start", datetime.now())
    with open('./%s_string_pair_markdown.tsv' % str(length), 'w') as wf:
        with open('./res_markdown.tsv') as f:
            for line in f.readlines():
                li = line.strip().split('\t')
                url, domain, qindex, question, answer = li
                # answers = li[4:]
                answer = answer.replace('\\n', '\n')
                question = question.replace('\\n', '\n')
                for s in split_to_word(question):
                    wf.write(f"{url}\t{domain}\t{qindex}\tQ\t{s}\n")
                for s in split_to_word(answer):
                    wf.write(f"{url}\t{domain}\t{qindex}\tA\t{s}\n")
                # for answer in answers:
                #     answer = answer.replace('\\n', '\n')
                #     for s in split_to_word(answer):
                #         wf.write(f"{url}\t{domain}\t{qindex}\tA\t{s}\n")
    print("end:", datetime.now())

