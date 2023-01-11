import glob
import json
import subprocess

from tqdm import tqdm

def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

for s in ["val", "test", "train"]:

    with open('/home/sajad/packages/sequential_sentence_classification/pubmedL.long.'+ s + '.json') as F:
        for l in tqdm(F, total=file_len('/home/sajad/packages/sequential_sentence_classification/pubmedL.long.'+ s + '.json')):
            papers_sects = {}
            paper = json.loads(l.strip())
            paper_id = paper['segment_id']
            paper_labels = paper['labels']

            for idx, sent_sect_label in enumerate(paper_labels):
                papers_sects[idx] = sent_sect_label

            try:
                SET="val"
                origin_paper = json.load(open("/disk1/sajad/datasets/sci/pubmedL/splits/" + SET + "/{}".format(paper_id.replace('.nxml', '.json'))))
            except:
                try:
                    SET = "test"
                    origin_paper = json.load(open("/disk1/sajad/datasets/sci/pubmedL/splits/" + SET + "/{}".format(
                        paper_id.replace('.nxml', '.json'))))
                except:
                    try:
                        SET = "train"
                        origin_paper = json.load(open("/disk1/sajad/datasets/sci/pubmedL/splits/" + SET + "/{}".format(
                            paper_id.replace('.nxml', '.json'))))
                    except:
                        continue


            new_sents = []
            for idx, sent in enumerate(origin_paper['sentences']):
                try:
                    sent = sent[0:5]
                    sent.append(papers_sects[idx])
                except:
                    sent.append(4)

                new_sents.append(sent)
            origin_paper['sentences'] = new_sents
            json.dump(origin_paper, open("/disk1/sajad/datasets/sci/pubmedL/splits/" + SET + "/{}".format(paper_id.replace('.nxml', '.json')), mode='w'))



