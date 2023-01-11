import glob

import torch
from tqdm import tqdm

intro_labels = {}
intro_len = {}
new_instances = []
DATASET='arxivL'
for s in ["train"]:
    for file in tqdm(glob.glob(f"/disk1/sajad/datasets/sci/{DATASET}/bert-files/2048-segmented-intro1536-15/{s}*.pt")):
        new_instances = []
        instances = torch.load(file)
        for instance in instances:
            intro_labels[instance['paper_id'].split('___')[0]] = sum(instance['intro_labels'])
            intro_len[instance['paper_id'].split('___')[0]] = len(instance['intro_labels'])

            # if len(instance['intro_labels']) < 8:
            #     continue
            # else:
            #     new_instances.append(instance)
        # torch.save(new_instances, file)

for k, v in intro_len.items():
    if v<8:
        print(k)
        print(v)
        # import pdb;pdb.set_trace()
import statistics

print('mean: {}, median: {}'.format(statistics.mean(intro_labels.values()), statistics.median(intro_labels.values())))
print('mean: {}, median: {}'.format(statistics.mean(intro_len.values()), statistics.median(intro_len.values())))

print(min(intro_len.values()))