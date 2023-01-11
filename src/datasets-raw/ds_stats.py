import glob
import json
import os
from operator import itemgetter

from tqdm import tqdm

from utils.rouge_score import evaluate_rouge


for f in glob.glob('longsumm/my-format-splits/train/*.json'):
    if ' ' not in f:
        continue
    f = "longsumm/my-format-splits/train/Unsupervised Neural Machine Translation with Weight Sharing.json"
    with open(f) as F:
        for l in F:
            entity = json.loads(l.strip())

            gold_sentences = [' '.join(e) for e in entity["gold"]]


            if len(gold_sentences) > 19 and len(gold_sentences) < 40:

                sections_sentences = [s[1] for s in entity['sentences']]

                sections_ordered = list(dict.fromkeys(sections_sentences))

                isConcAvailable = False
                isIntroAvailable = False
                for s in sections_ordered:
                    s = s.lower()
                    if 'conclusion' in s:
                        isConcAvailable = True
                    if 'introduction' in s:
                        isIntroAvailable = True

                if not isConcAvailable or not isIntroAvailable:
                    continue

                print('--- Paper name: {}'.format(f.split('/')[-1]))

                print('--- Sections list: \n ')
                print(', '.join([s for s in sections_ordered]))

                sections_sentences = {}

                for sent in entity['sentences']:
                    sent_text = sent[3]

                    if sent[1] not in sections_sentences.keys():
                        sections_sentences[sent[1]] = []

                    sections_sentences[sent[1]].append(sent_text)


                gold_sent_info = {}

                for gold_sent_number, gold_sent in tqdm(enumerate(gold_sentences), total=len(gold_sentences)):

                    # if gold_sent_number not in gold_sent_info.keys():
                    #     gold_sent_info[str(gold_sent_info)] = []


                    all_sents_with_rg = []
                    for section, sents in sections_sentences.items():
                        for sent in sents:
                            all_sents_with_rg.append((section, sent, evaluate_rouge([sent], [gold_sent])[1] + evaluate_rouge([sent], [gold_sent])[2]))

                    # sorted(all_sents_with_rg, key=itemgetter(2))
                    all_sents_with_rg = sorted(all_sents_with_rg, key=lambda x: x[2], reverse=True)
                    top_sections_for_gold_sent = [(s[0], s[-1]) for s in all_sents_with_rg[:10]]

                    gold_sent_info[str(gold_sent_number)] = top_sections_for_gold_sent


                # for sent_num, sent in enumerate(gold_sentences):

                    intro_sents = gold_sentences[:9]
                    detailed_sent = gold_sentences[9:]

                    most_similar = {}

                    for sent_num, isent in enumerate(intro_sents):
                        if sent_num == 2:
                            isent= "Motivated by recent success in unsupervised cross-lingual embeddings (Artetxe et al., 2016; Zhang et al., 2017b; Conneau et al., 2017), the models proposed for unsupervised NMT often assume that a pair of sentences from two different languages can be mapped to a same latent representation in a shared-latent space (Lample et al., 2017; Artetxe et al., 2017b)"

                        if sent_num == 0:
                            isent= "Neural machine translation (Kalchbrenner and Blunsom, 2013; Sutskever et al., 2014; Cho et al., 2014; Bahdanau et al., 2014), directly applying a single neural network to transform the source sentence into the target sentence, has now reached impressive performance."




                        most_similar_from_rest = []
                        for s_num_det, sent in enumerate(detailed_sent):
                            most_similar_from_rest.append((sent, evaluate_rouge([sent], [isent])[1] + evaluate_rouge([sent], [isent])[2]))

                        most_similar_from_rest = sorted(most_similar_from_rest, key=lambda x: x[1], reverse=True)
                        most_similar[str(sent_num)] = most_similar_from_rest
                        s = 0

                # foor sent_num, sent in gold_sent_info:
                # intro_sents =


