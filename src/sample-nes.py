import csv
import json
import random

import pandas as pd

old_samples = []

with open("arxivL-samples.txt") as fR:
    for l in fR:
        old_samples.append(l)

bertsumsext_summaries = {}
oracle_summaries = {}

with open('../test-new.json') as fR:
    for l in fR:
        ent = json.loads(l)
        oracle_summaries[ent['id']] = ent['abstract']

with open('anal_outputs/results_arxivL-test-BertSumExt.p.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for j, row in enumerate(spamreader):
        if j == 0: continue
        # print(', '.join(row))
        bertsumsext_summaries[row[0]] = json.loads(row[1])

bertsumextIntro_summaries = {}
with open('anal_outputs/results_arxivL-test-BertSumIntroGuided.p.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for j, row in enumerate(spamreader):
        if j == 0: continue
        bertsumextIntro_summaries[row[0]] = json.loads(row[1])
    # print(', '.join(row))

samples = []
sample_ordering = []
counter = 0
for id, pred in bertsumsext_summaries.items():
    if id not in old_samples and id in oracle_summaries.keys():
        bertsumext_pred = ''
        for idx in sorted(pred.keys()):
            bertsumext_pred += pred[idx]['sentence']
            bertsumext_pred += ' '

        intro_pred = bertsumextIntro_summaries[id]
        bertsumextIntro_pred = ''
        for idx in sorted(intro_pred.keys()):
            bertsumextIntro_pred += intro_pred[idx]['sentence']
            bertsumextIntro_pred += ' '

        oracle_pred_ = oracle_summaries[id]

        counter += 1
        samples.append({'bertsumExt': bertsumext_pred, 'bertsumExtIntro': bertsumextIntro_pred, 'target': oracle_pred_})
        sample_ordering.append(["bertsumExt", "bertsumExtIntro"])
        if counter == 40:
            break

# re-ordering
new_samples = []
new_orders = []
for sample, ordering in zip(samples, sample_ordering):
    rand_int = random.randint(0, 1)
    new_order = [ordering[rand_int]] + [ordering[0 if rand_int == 1 else 1]]
    new_orders.append(new_order)
    new_samples.append((sample[new_order[0]], sample[new_order[1]], sample['target']))


with open('anal_outputs/new_orders.txt', mode='w') as fW:
    for n in new_orders:
        fW.write(str(n))
        fW.write('\n')

df = pd.DataFrame(
    {
        'pred_1': [s[0] for s in new_samples],
        'pred_2': [s[1] for s in new_samples],
        'target': [s[2] for s in new_samples],
    }
)

df.to_csv('anal_outputs/new_samples.csv')