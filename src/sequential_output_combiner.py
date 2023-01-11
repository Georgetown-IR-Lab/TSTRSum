import collections
import json

instance_labels_old = collections.defaultdict(dict)
instance_labels_new = collections.defaultdict(dict)


PREDICTED_LABELS = "/home/sajad/packages/sequential_sentence_classification"
for se in ["test", "train"]:
    with open(PREDICTED_LABELS + "/LSUM.long." + se + ".json") as F:
        for l in F:
            inst = json.loads(l.strip())
            # ds_instance_labels.append(inst)
            for i, s in enumerate(inst['sentences']):
                instance_labels_old[inst['segment_id']][i] = inst['labels'][i]



    with open(PREDICTED_LABELS + "/longsumm.long.part." + se + ".json") as FF:
        for l in FF:
            inst = json.loads(l.strip())
            # ds_instance_labels.append(inst)
            for i, s in enumerate(inst['sentences']):
                instance_labels_new[inst['segment_id']][i] = inst['labels'][i]


    for key, val in instance_labels_new.items():
        instance_labels_old[key] = val


    with open(PREDICTED_LABELS + "/LSUM.long.combined." + se + ".json", mode='w') as FFF:
        json.dump(instance_labels_old, FFF)