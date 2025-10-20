import csv
import json
import random
from datetime import datetime


category_with_questions = {}
with open('category_with_question.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        category_1 = row["一级分类"]
        category_2 = row["二级分类"]
        q = row['问题']
        q_id = row['编号']
        answer_source = row['生成答案的方式']
        info = f"{q}\t{category_1}>{category_2}\t{answer_source}\t{q_id}"
        if category_1 not in category_with_questions:
            category_with_questions[category_1] = {}
        if category_2 in category_with_questions[category_1]:
            category_with_questions[category_1][category_2].append(info)
        else:
            category_with_questions[category_1][category_2] = [info]

conflict_categories = {}
with open('conflict_category.json') as f:
    for k, v in json.load(f).items():
        k = k.lower()
        for c in v:
            c = c.lower()
            if c not in conflict_categories:
                conflict_categories[c] = []
            conflict_categories[c].append(k)


store_with_category = {}
with open('store_with_category.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        store = row['domain']
        category = row['类别']
        assert store not in store_with_category and category, row
        store_with_category[store] = category


def _get_question(c_1, c_2_count=1, store_category=None):
    sub_categories = list(category_with_questions[c_1].keys())
    if store_category in conflict_categories:
        sub_categories = list(filter(lambda c: c not in conflict_categories[store_category], sub_categories))
    for c_2 in random.sample(sub_categories, c_2_count):
        yield random.choice(category_with_questions[c_1][c_2])


def main():
    with open("query_res_%s.tsv" % datetime.now().strftime("%Y-%m-%d"), 'w') as f:
        with open('store_with_url.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                store = row['store domain']
                url = row['coupon url']
                store_category = store_with_category.get(store, '').lower()
                random.seed(url)
                for q_1_info in _get_question('coupons & sales', 1, store_category):
                    f.write(f"{url}\t{store}\t{q_1_info}\t\t\n")
                for q_2_info in _get_question('特殊优惠', 2, store_category):
                    if '手写模板' in q_2_info:
                        if 'military discount' in q_2_info:
                            f.write(f"{url}\t{store}\t{q_2_info}\tTrue\t\n")
                            f.write(f"{url}\t{store}\t{q_2_info}\tFalse\t\n")
                        elif 'student discount' in q_2_info:
                            f.write(f"{url}\t{store}\t{q_2_info}\t\tTrue\n")
                            f.write(f"{url}\t{store}\t{q_2_info}\t\tFalse\n")
                        else:
                            f.write(f"{url}\t{store}\t{q_2_info}\t\t\n")
                    else:
                        f.write(f"{url}\t{store}\t{q_2_info}\t\t\n")
                for q_3_info in _get_question('会员优惠 & 商家政策', 1, store_category):
                    f.write(f"{url}\t{store}\t{q_3_info}\t\t\n")


if __name__ == "__main__":
    main()