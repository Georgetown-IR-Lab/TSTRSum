# bertsumIntro_output = {}
# golds = {}
#
# with open('../test_step2231.json') as F:
#     for l in F:
#         ent = json.loads(l)
#
#         bertsumIntro_output[ent['paper_id']] = ent['pred']
#         golds[ent['paper_id']] = ent['gold']
#
# # with open('../test-new.json') as F:
# #     for l in F:
# #         ent = json.loads(l)
# #         if ent['id'] != -1:
# #             bart_output[ent['id']] = ent['text']
#
# bart_output = {}
# with open('../test-new.json') as fS, open('../generated_predictions.txt') as fT:
#     for lS, lT in zip(fS, fT):
#         ent = json.loads(lS)
#
#         if ent['id'] != -1:
#             bart_output[ent['id']] = lT.strip()
#         else:
#             continue
#
# parallel_list_unsort = []
#
# for id, bart_pred in tqdm(bart_output.items(), total=len(bart_output)):
#     bert_pred = bertsumIntro_output[id]
#     bart_rg = evaluate_rouge([bart_pred], [golds[id]])[-1]
#     bert_rg = evaluate_rouge([bert_pred], [golds[id]])[-1]
#     parallel_list_unsort.append((id, golds[id], bart_pred, bart_rg, bert_pred, bert_rg, bart_rg - bert_rg))
#
# parallel_list_sort = sorted(parallel_list_unsort, key=itemgetter(6), reverse=True)
#
# iter = 0
# bin_count = 100
# bin_size = len(parallel_list_sort) // bin_count
# pointer = 0
#
# sampled = []
#
# while pointer < len(parallel_list_sort):
#     start_idx = pointer
#     end_idx = (iter * bin_count) + bin_size
#
#     if end_idx > len(parallel_list_sort):
#         end_idx = len(parallel_list_sort)
#
#     rand_idx = random.randint(start_idx, end_idx)
#
#     sample = parallel_list_sort[rand_idx]
#     sampled.append(sample)
#
#     pointer += bin_size
#     iter += 1
#
#     if len(sampled) == bin_count:
#         break

# sample_dct = {
#     'id': [],
#     'gold': [],
#     'bart_pred': [],
#     'bart_rgL': [],
#     'bert_pred': [],
#     'bert_rgL': [],
#     'rgL_diff': [],
# }

# for s in sampled:
#     id, gold, bart_output, bart_rg, bert_pred, bert_rg, rgL_diff = s
#
#     sample_dct['id'].append(id)
#     sample_dct['gold'].append(gold)
#     sample_dct['bart_pred'].append(bart_output)
#     sample_dct['bart_rgL'].append(bart_rg)
#     sample_dct['bert_pred'].append(bert_pred)
#     sample_dct['bert_rgL'].append(bert_rg)
#     sample_dct['rgL_diff'].append(rgL_diff)
import random

import pandas as pd

# df = pd.DataFrame(sample_dct, columns=['id', 'gold', 'bart_pred', 'bart_rgL', 'bert_pred', 'bert_rgL', 'rgL_diff'])
# df.to_csv(r'../arXivL_BartBert.csv', index=False, header=True)

df = pd.read_csv(r'../arXivL_BartBert.csv',
                 usecols=['id', 'gold', 'bart_pred', 'bart_rgL', 'bert_pred', 'bert_rgL', 'rgL_diff'])

idx = [0, 1]
id_file = open('id_file.txt', mode='a')

shuffled_lst = {
    'id': [],
    'gold': [],
    'pred1': [],
    'rgL1': [],
    'pred2': [],
    'rgL2': [],
}

for i in range(0, len(df)):
    id = df.iloc[i]['id']
    gold = df.iloc[i]['gold']
    bart_pred = df.iloc[i]['bart_pred']
    bart_rgL = df.iloc[i]['bart_rgL']
    bert_pred = df.iloc[i]['bert_pred']
    bert_rgL = df.iloc[i]['bert_rgL']
    rgL_diff = df.iloc[i]['rgL_diff']

    rand_idx = random.randint(0, 1)
    shuffled_outputs_before = [(bart_pred, bart_rgL), (bert_pred, bert_rgL)]

    if rand_idx==0:
        id_file.write('bart')
        id_file.write('\n')

        shuffled_lst['id'].append(id)
        shuffled_lst['gold'].append(gold)
        shuffled_lst['pred1'].append(bart_pred)
        shuffled_lst['rgL1'].append(bart_rgL)
        shuffled_lst['pred2'].append(bert_pred)
        shuffled_lst['rgL2'].append(bert_rgL)

    else:
        id_file.write('bertSum')
        id_file.write('\n')

        shuffled_lst['id'].append(id)
        shuffled_lst['gold'].append(gold)
        shuffled_lst['pred1'].append(bert_pred)
        shuffled_lst['rgL1'].append(bert_rgL)
        shuffled_lst['pred2'].append(bart_pred)
        shuffled_lst['rgL2'].append(bart_rgL)


df = pd.DataFrame(shuffled_lst, columns=['id', 'gold', 'pred1', 'rgL1', 'pred2', 'rgL2'])
df.to_csv(r'../arXivL_BartBert_modfied.csv', index=False, header=True)
