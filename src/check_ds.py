import glob
import json

# with open("/disk1/sajad/datasets/sci/arxivL/bart/whole/test.json") as FL:
bart_instances = []
summ_to_src_map = {}
with open("../test.json") as FL:
    for l in FL:
        ent = json.loads(l.strip())
        summ_to_src_map[''.join(ent['abstract'].split()[:10])] = ent['text']
        summ_to_src_map[''.join(ent['abstract'].split()[:8])] = ent['text']
        bart_instances.append(ent)

summ_to_id_map = {}

for f in glob.glob('datasets-raw//arxivL/splits/test/*.json'):
    with open(f) as F:
        for l in F:
            ent = json.loads(l)

            w10summ = ''.join(ent['gold'][0][:10])
            w8summ = ''.join(ent['gold'][0][:8])

            summ_to_id_map[w10summ] = ent['id']
            summ_to_id_map[w8summ] = ent['id']

passed = 0
for key, val in summ_to_src_map.items():
    try:
        id = summ_to_id_map[key]
    except:
        print(f'passed {passed}')
        passed+=1


new_instances = []
for inst in bart_instances:
    try:
        src = inst['text']
        summary = inst['abstract']
        w10summ = ''.join(summary.split()[:10])
        id = summ_to_id_map[w10summ]

        new_instances.append({'id':id, 'text': src, 'abstract':summary})
    except:
        try:
            w8summ = ''.join(summary.split()[:8])
            id = summ_to_id_map[w8summ]
            new_instances.append({'id':id, 'text': src, 'abstract':summary})
        except:
            new_instances.append({'id':-1, 'text': src, 'abstract':summary})
            continue

with open("../test-new.json", mode='w') as FL:
    for b in new_instances:
        json.dump(b, FL)
        FL.write('\n')