from six_tuple_calculate import length

if __name__ == '__main__':
    res_map = {}
    with open('./res_markdown.tsv') as f:
        for line in f.readlines():
            li = line.strip().split('\t')
            question = li[3]
            answer = li[4]
            # answer = '\\n'.join(li[4:])
            key = '_'.join(li[:3])
            res_map[key] = {'Q': question, 'A': answer}

    seg_map = {}
    with open('./%s_string_pair_markdown.tsv' % str(length)) as f:
        for line in f.readlines():
            li = line.strip().split('\t')
            seg = li[-1]
            key = '_'.join(li[:3])
            qtype = li[3]
            info = ' '.join(li[:-1])
            if seg not in seg_map:
                seg_map[seg] = [info, res_map[key]['Q']]
            elif seg in seg_map:
                seg_map[seg].append(info)
                seg_map[seg].append(res_map[key]['Q'])

    with open('./top_%s_markdown' % str(length)) as f:
        for line in f.readlines():
            count, seg = line.strip().split('\t')
            samples = seg_map[seg][:10]
            print(seg, '\t'.join(samples), sep='\t')
