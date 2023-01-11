import json

with open("/disk1/sajad/datasets/sci/arxivL/splits-with-sections-introConc/val/1606.00337.json", mode='r') as F:

    paper = json.load(F)
    sent_labels = [s[-2] for s in paper["sentences"]]
    import pdb;pdb.set_trace()

