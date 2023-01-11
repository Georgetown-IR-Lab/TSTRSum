import json

paper_ids = []
sampled = []

# with open("arxivL-anal-paperIDs.txt") as F:
#     for l in F:
#         paper_ids.append(l.strip())
#
from random import randrange
#
# foo = ['a', 'b', 'c', 'd', 'e']
# print(random.choice(foo))
#
# SAMPLED_NUM = 40
# bin_size = len(paper_ids) // SAMPLED_NUM
# iteration = 1
#
# while iteration < 41:
#     current_list = paper_ids[(iteration-1)*bin_size: iteration*bin_size]
#     sampled.append(random.choice(current_list))
#     print(str(iteration) + '. ' +  sampled[-1])
#     iteration+=1
#
# with open("arxivL-samples.txt", mode='w') as FF:
#     for sl in sampled:
#         FF.write(sl)
#         FF.write('\n')

sampled_paperIDs = []
target = []
ours = []
bs = []

with open("arxivL-samples.txt") as F:
    for l in F:
        sampled_paperIDs.append(l.strip())

with open("pred_target.txt") as F:
    for l in F:
        target.append(l.strip())

with open("pred_ours.txt") as F:
    for l in F:
        ours.append(l.strip())

with open("pred_bs.txt") as F:
    for l in F:
        bs.append(l.strip())


final_list = []
for p_id, t, o, b in zip(sampled_paperIDs, target, ours, bs):
    tmp_list = []
    tmp_list.extend([{'type':'ours', 'pred':o}, {'type':'baseline', 'pred':b}])
    random_index = randrange(len(tmp_list))

    first_pred = tmp_list[random_index]['pred']
    first_type = tmp_list[random_index]['type']

    second_idx = [idx for idx, t in enumerate(tmp_list) if idx!=random_index][0]
    second_pred = tmp_list[second_idx]['pred']
    second_type = tmp_list[second_idx]['type']
    json_file = {"paper_id": p_id,
                 "pred_1": first_pred,
                 "pred_2":second_pred,
                 "target": t,
                 "order": str((first_type, second_type))}
    s=0

    final_list.append(json_file)

with open('arxivL-anal.json', mode='w') as FFF:
    for j in final_list:
        json.dump({"paper_id": j["paper_id"],
                 "pred_1": j["pred_1"],
                 "pred_2":j["pred_2"],
                 "target": j["target"]}, FFF, indent=4)
        FFF.write('\n')

with open('arxivL-anal-blind.json', mode='w') as FFF:
    for j in final_list:
        del j['pred_1']
        del j['pred_2']
        del j['target']
        json.dump(j, FFF, indent=4)
        FFF.write('\n')